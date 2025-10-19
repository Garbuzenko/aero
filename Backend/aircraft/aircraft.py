import threading
from datetime import datetime
import time
import json
import schedule

import mysql.connector
from mysql.connector import errorcode, pooling

from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.prepared import prep
import rtree
from functools import lru_cache
import sys
import os
import re

# from aircraft.opensky_client import OpenSkyClient
from .opensky_client import OpenSkyClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from .polygon_processor import PolygonProcessor

from settings import DB_CONFIG


# ======================
# Глобальное состояние с блокировкой
# ======================
spatial_index = None
region_polygons = {}
_regions_loaded = False
_regions_lock = threading.Lock()


class DatabaseManager:
    def __init__(self, config):
        self.connection_pool = None
        self.init_connection_pool(config)

    def init_connection_pool(self, config):
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="mysql_pool",
                pool_size=10,
                pool_reset_session=True,
                **config
            )
            print("Пул соединений с MySQL успешно инициализирован")
            return True
        except mysql.connector.Error as err:
            print(f"Ошибка при создании пула соединений: {err}")
            return False

    def get_connection(self):
        if self.connection_pool:
            try:
                return self.connection_pool.get_connection()
            except mysql.connector.Error as err:
                print(f"Ошибка при получении соединения из пула: {err}")
        return None

    def safe_execute(self, cursor, query, params=None, max_retries=3):
        for attempt in range(max_retries):
            try:
                cursor.execute(query, params or ())
                return True
            except mysql.connector.Error as err:
                if err.errno in (errorcode.CR_SERVER_LOST, errorcode.CR_CONNECTION_ERROR):
                    print(f"Потеряно соединение (попытка {attempt + 1}/{max_retries})")
                    time.sleep(2 ** attempt)
                    continue
                else:
                    print(f"Ошибка MySQL: {err}")
                    return False
        return False

    def safe_executemany(self, cursor, query, params, max_retries=3):
        for attempt in range(max_retries):
            try:
                cursor.executemany(query, params)
                return True
            except mysql.connector.Error as err:
                if err.errno in (errorcode.CR_SERVER_LOST, errorcode.CR_CONNECTION_ERROR):
                    print(f"Потеряно соединение (попытка {attempt + 1}/{max_retries})")
                    time.sleep(2 ** attempt)
                    continue
                else:
                    print(f"Ошибка MySQL при массовой вставке: {err}")
                    return False
        return False


def load_regions():
    """Загружает полигоны регионов из БД и строит пространственный индекс."""
    global spatial_index, region_polygons, _regions_loaded

    with _regions_lock:
        if _regions_loaded:
            return True

        db_manager = DatabaseManager(DB_CONFIG)
        conn = db_manager.get_connection()
        if not conn:
            print("Не удалось подключиться к БД для загрузки регионов")
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, polygon FROM regions")
            regions_data = cursor.fetchall()

            spatial_index = rtree.Index()
            region_polygons = {}

            for region_id, polygon_str in regions_data:
                try:
                    polygons_data = json.loads(polygon_str)
                    polygons = []
                    for poly_data in polygons_data:
                        coords = [(point[1], point[0]) for point in poly_data]  # (lon, lat)
                        polygon = Polygon(coords)
                        if polygon.is_valid:
                            polygons.append(polygon)

                    if polygons:
                        multi_polygon = MultiPolygon(polygons)
                        for polygon in polygons:
                            spatial_index.insert(region_id, polygon.bounds)
                        region_polygons[region_id] = prep(multi_polygon)

                except Exception as e:
                    print(f"Ошибка обработки региона {region_id}: {e}")

            _regions_loaded = True
            print(f"Загружено {len(region_polygons)} регионов")
            return True

        except Exception as e:
            print(f"Ошибка при загрузке регионов: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


@lru_cache(maxsize=10000)
def get_region_id(lat, lon):
    """Возвращает идентификатор региона для заданных координат."""
    if lat is None or lon is None:
        return None

    if not _regions_loaded:
        if not load_regions():
            return None

    if spatial_index is None or not region_polygons:
        return None

    point = Point(lon, lat)
    candidate_ids = set(spatial_index.intersection((lon, lat, lon, lat)))

    for region_id in candidate_ids:
        if region_id in region_polygons and region_polygons[region_id].contains(point):
            return region_id
    return None


class RegionRatingCalculator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

class AircraftDataProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def parse_aircraft_data(self, raw_data):
        if not raw_data or 'states' not in raw_data:
            return []

        aircraft_list = []
        for state in raw_data['states']:
            if not state or len(state) < 17:
                continue

            try:
                aircraft = {
                    'icao24': state[0] or 'N/A',
                    'callsign': (state[1] or 'N/A').strip(),
                    'country': state[2] or 'N/A',
                    'timestamp': datetime.fromtimestamp(state[3]) if state[3] else None,
                    'last_contact': datetime.fromtimestamp(state[4]) if state[4] else None,
                    'longitude': state[5] if state[5] is not None else 0,
                    'latitude': state[6] if state[6] is not None else 0,
                    'altitude': state[7] if state[7] is not None else 0,
                    'on_ground': bool(state[8]) if state[8] is not None else False,
                    'velocity': state[9] if state[9] is not None else 0,
                    'heading': state[10] if state[10] is not None else 0,
                    'vertical_rate': state[11] if state[11] is not None else 0,
                    'sensors': state[12] or [],
                    'geo_altitude': state[13] if state[13] is not None else 0,
                    'squawk': state[14] or 'N/A',
                    'spi': bool(state[15]) if state[15] is not None else False,
                    'position_source': state[16] if state[16] is not None else 0,
                    'timestamp_utc': datetime.utcnow()
                }
                aircraft_list.append(aircraft)
            except (IndexError, TypeError, ValueError, OSError) as e:
                print(f"Ошибка парсинга самолета: {e}")
                continue

        return aircraft_list

    def insert_aircraft_data(self, aircraft_list):
        if not aircraft_list:
            return 0

        insert_query = """
        INSERT INTO aircraft (
            icao24, callsign, country, timestamp, last_contact,
            longitude, latitude, altitude, on_ground, velocity,
            heading, vertical_rate, geo_altitude, squawk, spi,
            position_source, timestamp_utc, utc_int, active, region_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        connection = self.db_manager.get_connection()
        if not connection:
            print("Не удалось получить соединение с БД")
            return 0

        cursor = connection.cursor()
        successful_inserts = 0
        batch_size = 1000

        try:
            for i in range(0, len(aircraft_list), batch_size):
                batch = aircraft_list[i:i + batch_size]
                data_to_insert = []

                for aircraft in batch:
                    utc_int = int(aircraft['timestamp_utc'].timestamp())
                    lat = aircraft['latitude']
                    lon = aircraft['longitude']
                    region_id = get_region_id(lat, lon) if lat and lon else None

                    data_to_insert.append((
                        aircraft['icao24'],
                        aircraft['callsign'],
                        aircraft['country'],
                        aircraft['timestamp'],
                        aircraft['last_contact'],
                        aircraft['longitude'],
                        aircraft['latitude'],
                        aircraft['altitude'],
                        aircraft['on_ground'],
                        aircraft['velocity'],
                        aircraft['heading'],
                        aircraft['vertical_rate'],
                        aircraft['geo_altitude'],
                        aircraft['squawk'],
                        aircraft['spi'],
                        aircraft['position_source'],
                        aircraft['timestamp_utc'],
                        utc_int,
                        1,
                        region_id
                    ))

                if self.db_manager.safe_executemany(cursor, insert_query, data_to_insert):
                    connection.commit()
                    inserted = len(batch)
                    successful_inserts += inserted
                    print(f"Добавлено {inserted} записей в aircraft")
                else:
                    print(f"Не удалось вставить пакет из {len(batch)} записей")
                    connection.rollback()

            return successful_inserts

        except Exception as e:
            print(f"Ошибка при вставке данных: {e}")
            # connection.rollback()
            return successful_inserts
        finally:
            cursor.close()
            connection.close()


class Scheduler:
    def __init__(self, db_manager, opensky_client, aircraft_processor):
        self.db_manager = db_manager
        self.opensky_client = opensky_client
        self.aircraft_processor = aircraft_processor
        self.rating_calculator = RegionRatingCalculator(db_manager)

    def update_active(self):
        query_max = "SELECT MAX(utc_int) FROM aircraft"
        query_update = """
            UPDATE aircraft 
            SET active = IF((%s - utc_int) > 500, 0, 1) 
            WHERE active = 1
        """

        connection = self.db_manager.get_connection()
        if not connection:
            print("Не удалось получить соединение с БД")
            return 0

        try:
            cursor = connection.cursor()
            cursor.execute(query_max)
            max_utc = cursor.fetchone()[0]

            if max_utc is None:
                print("Таблица aircraft пуста")
                return 0

            cursor.execute(query_update, (max_utc,))
            connection.commit()
            updated_count = cursor.rowcount
            print(f"Обновлено записей: {updated_count}")
            return updated_count

        except Exception as e:
            print(f"Ошибка при обновлении active: {e}")
            connection.rollback()
            return 0
        finally:
            cursor.close()
            connection.close()

    def fetch_and_save_aircraft_data(self):
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Получение данных о самолетах...")
        bbox = 0  # Весь мир
        simple_data = self.opensky_client.get_all_aircrafts(bbox=bbox)

        if simple_data and 'states' in simple_data:
            print(f"Самолетов найдено: {len(simple_data['states'])}")
            parsed_data = self.aircraft_processor.parse_aircraft_data(simple_data)
            self.aircraft_processor.insert_aircraft_data(parsed_data)

            if parsed_data:
                print(f"Данные сохранены. Время: {datetime.now().strftime('%H:%M:%S')}")
                for i, ac in enumerate(parsed_data[:3]):
                    print(f"   {i + 1}. {ac.get('callsign', 'N/A')} - "
                          f"({ac.get('latitude', 0):.4f}, {ac.get('longitude', 0):.4f})")
            else:
                print("Нет данных для сохранения")
        else:
            print("Не удалось получить данные от OpenSky")

        self.update_active()

    def scheduled_aircraft_data_fetch(self, interval=300):
        schedule.every(interval).seconds.do(self.fetch_and_save_aircraft_data)
        self.fetch_and_save_aircraft_data()  # Первый запуск сразу
        print(f"Запущен сбор данных каждые {interval} секунд. Ctrl+C для остановки")

        try:
            while True:
                schedule.run_pending()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nОстановка...")

    def start_aircraft_data_thread(self, interval=300):
        thread = threading.Thread(
            target=self.scheduled_aircraft_data_fetch,
            args=(interval,),
            daemon=True
        )
        thread.start()
        return thread


def main():
    try:
        db_manager = DatabaseManager(DB_CONFIG)
        if not db_manager.connection_pool:
            print("Ошибка инициализации пула соединений")
            return

        opensky_client = OpenSkyClient()
        aircraft_processor = AircraftDataProcessor(db_manager)
        scheduler = Scheduler(db_manager, opensky_client, aircraft_processor)

        # Запуск потока сбора данных
        aircraft_thread = scheduler.start_aircraft_data_thread(interval=600)

        # Обработка полигонов (однократно)
        # Нет смысла постоянно запускать, временно отключил
        if 1 == 2:
            polygon_processor = PolygonProcessor(db_manager)
            print("Запуск обработки полигонов России...")
            polygon_processor.set_points_polygon()
            polygon_processor.calculate_intersections()
            print("Обработка полигонов завершена. Сбор данных продолжается...")

        # Ожидание
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nЗавершение работы...")

    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        print("Программа завершена")


if __name__ == "__main__":
    main()