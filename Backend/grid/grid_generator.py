# grid_generator.py
import mysql.connector
from mysql.connector import Error
import math
from typing import List, Tuple
import logging
from decimal import Decimal, ROUND_HALF_UP
import time
import json
import h3

from settings import DB_CONFIG

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../parser/log.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GridGenerator:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.default_area = 1000  # км² по умолчанию
        self.regions = []  # Кэш регионов России

    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            logger.info("Успешное подключение к базе данных")
            return True
        except Error as e:
            logger.error(f"Ошибка подключения: {e}")
            return False

    def check_table_exists(self, table_name):
        """Проверяет существование таблицы"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            return cursor.fetchone() is not None
        except Error as e:
            logger.error(f"Ошибка проверки таблицы {table_name}: {e}")
            return False

    def drop_grid_tables(self):
        """Удаление таблиц сеток если они существуют"""
        try:
            cursor = self.connection.cursor()
            if self.check_table_exists('grid_square'):
                cursor.execute("DROP TABLE grid_square")
                logger.info("Таблица grid_square удалена")
            if self.check_table_exists('grid_hexagon'):
                cursor.execute("DROP TABLE grid_hexagon")
                logger.info("Таблица grid_hexagon удалена")
            self.connection.commit()
            return True
        except Error as e:
            logger.error(f"Ошибка удаления таблиц: {e}")
            return False

    def create_settings_table(self):
        """Создание или обновление таблицы настроек"""
        try:
            cursor = self.connection.cursor()

            # Проверяем существование таблицы
            if not self.check_table_exists('settings'):
                cursor.execute("""
                    CREATE TABLE settings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        key_name VARCHAR(50) UNIQUE NOT NULL,
                        value VARCHAR(255) NOT NULL,
                        description TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB
                """)
                logger.info("Таблица settings создана")

            # Добавляем значение по умолчанию
            cursor.execute("""
                INSERT IGNORE INTO settings (key_name, value, description)
                VALUES ('grid_cell_area', '1000', 'Площадь ячейки сетки в км²')
            """)

            self.connection.commit()
            logger.info("Таблица настроек проверена/обновлена")
            return True
        except Error as e:
            logger.error(f"Ошибка работы с таблицей настроек: {e}")
            return False

    def get_grid_cell_area(self) -> float:
        """Получение размера ячейки из настроек"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT value FROM settings WHERE key_name = 'grid_cell_area'")
            result = cursor.fetchone()
            return float(result[0]) if result else self.default_area
        except Error as e:
            logger.error(f"Ошибка получения настроек: {e}")
            return self.default_area

    def load_russia_regions(self):
        """Загрузка регионов России из базы данных"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, polygon FROM regions")
            self.regions = cursor.fetchall()
            logger.info(f"Загружено {len(self.regions)} регионов России")
            return True
        except Error as e:
            logger.error(f"Ошибка загрузки регионов: {e}")
            return False

    def is_point_in_russia(self, lat: float, lon: float) -> bool:
        """Проверяет, находится ли точка на территории России"""
        if not self.regions:
            return False

        # Преобразуем координаты в строку для сравнения
        point_str = f"{lat},{lon}"

        # Простая проверка по bounding box России
        if not (41.0 <= lat <= 82.0 and 19.0 <= lon <= 180.0):
            return False

        # Более точная проверка по регионам
        for region in self.regions:
            try:
                polygon = json.loads(region['polygon'])
                if self.is_point_in_polygon(lat, lon, polygon[0]):
                    return True
            except:
                continue

        return False

    def is_point_in_polygon(self, lat: float, lon: float, polygon: List[List[float]]) -> bool:
        """Проверяет, находится ли точка внутри полигона"""
        # Алгоритм ray casting
        inside = False
        n = len(polygon)

        if n < 3:
            return False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if lon > min(p1y, p2y):
                if lon <= max(p1y, p2y):
                    if lat <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (lon - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or lat <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def calculate_cell_size(self, area_km2: float, latitude: float = 55.0) -> Tuple[float, float]:
        """
        Расчет размера ячейки в градусах по площади
        latitude - средняя широта для региона (по умолчанию 55.0 для России)
        """
        # 1 градус широты = 111.32 км
        km_per_degree_lat = 111.32

        # 1 градус долготы = 111.32 * cos(latitude) км
        km_per_degree_lon = 111.32 * math.cos(math.radians(latitude))

        # Размер стороны квадрата в км
        side_km = math.sqrt(area_km2)

        # Размер в градусах
        lat_step = side_km / km_per_degree_lat
        lon_step = side_km / km_per_degree_lon

        return lat_step, lon_step

    def round_coordinate(self, value: float, precision: int = 8) -> float:
        """Округление координаты с заданной точностью"""
        decimal_value = Decimal(str(value))
        rounded = decimal_value.quantize(Decimal('1.' + '0' * precision), rounding=ROUND_HALF_UP)
        return float(rounded)

    def generate_square_polygon(self, center_lat: float, center_lon: float,
                                lat_step: float, lon_step: float) -> List[List[float]]:
        """Генерация квадратного полигона"""
        half_lat = lat_step / 2
        half_lon = lon_step / 2

        # Обеспечиваем корректный порядок координат [широта, долгота]
        return [
            [self.round_coordinate(center_lat - half_lat), self.round_coordinate(center_lon - half_lon)],
            [self.round_coordinate(center_lat - half_lat), self.round_coordinate(center_lon + half_lon)],
            [self.round_coordinate(center_lat + half_lat), self.round_coordinate(center_lon + half_lon)],
            [self.round_coordinate(center_lat + half_lat), self.round_coordinate(center_lon - half_lon)],
            [self.round_coordinate(center_lat - half_lat), self.round_coordinate(center_lon - half_lon)]
            # Замыкаем полигон
        ]

    def create_grid_tables(self):
        """Создание таблиц для хранения полигонов"""
        try:
            cursor = self.connection.cursor()

            # Таблица для квадратных полигонов
            cursor.execute("""
                CREATE TABLE grid_square (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    polygon LONGTEXT NOT NULL,
                    center_lat DECIMAL(11, 8) NOT NULL,
                    center_lon DECIMAL(11, 8) NOT NULL,
                    area_km2 FLOAT NOT NULL,
                    region_id INT,
                    total_flights INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_region_id (region_id),
                    INDEX idx_center (center_lat, center_lon),
                    INDEX idx_total_flights (total_flights)
                ) ENGINE=InnoDB
            """)
            logger.info("Таблица grid_square создана")

            # Таблица для шестиугольных полигонов
            cursor.execute("""
                CREATE TABLE grid_hexagon (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    polygon LONGTEXT NOT NULL,
                    center_lat DECIMAL(11, 8) NOT NULL,
                    center_lon DECIMAL(11, 8) NOT NULL,
                    area_km2 FLOAT NOT NULL,
                    region_id INT,
                    total_flights INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_region_id (region_id),
                    INDEX idx_center (center_lat, center_lon),
                    INDEX idx_total_flights (total_flights)
                ) ENGINE=InnoDB
            """)
            logger.info("Таблица grid_hexagon создана")

            self.connection.commit()
            logger.info("Таблицы сеток созданы")
            return True
        except Error as e:
            logger.error(f"Ошибка создания таблиц: {e}")
            return False

    def find_region_for_point(self, lat: float, lon: float) -> int:
        """Находит регион для точки"""
        for region in self.regions:
            try:
                polygon = json.loads(region['polygon'])
                if self.is_point_in_polygon(lat, lon, polygon[0]):
                    return region['id']
            except:
                continue
        return None

    def _generate_square_grid(self, min_lat, min_lon, max_lat, max_lon, lat_step, lon_step, area_km2):
        """Генерация квадратной сетки только для территории России"""
        cursor = self.connection.cursor()
        count = 0
        skipped = 0
        total_estimated = int((max_lat - min_lat) / lat_step * (max_lon - min_lon) / lon_step)
        start_time = time.time()
        last_log_time = start_time

        logger.info(f"Начинаем генерацию квадратной сетки, примерно {total_estimated} полигонов")

        # Генерируем новые полигоны
        lat = min_lat + lat_step / 2
        lat_index = 0

        while lat < max_lat:
            lon = min_lon + lon_step / 2
            while lon < max_lon:
                # Проверяем, находится ли центр полигона в России
                if not self.is_point_in_russia(lat, lon):
                    skipped += 1
                    lon += lon_step
                    continue

                # Округляем координаты центра
                rounded_lat = self.round_coordinate(lat)
                rounded_lon = self.round_coordinate(lon)

                # Находим регион для центра полигона
                region_id = self.find_region_for_point(rounded_lat, rounded_lon)
                if not region_id:
                    skipped += 1
                    lon += lon_step
                    continue

                polygon = self.generate_square_polygon(rounded_lat, rounded_lon, lat_step, lon_step)

                # Форматируем полигон в требуемом формате
                polygon_json = json.dumps([polygon])

                try:
                    cursor.execute("""
                        INSERT INTO grid_square (polygon, center_lat, center_lon, area_km2, region_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (polygon_json, rounded_lat, rounded_lon, area_km2, region_id))
                    count += 1

                    # Логируем прогресс каждые 1000 полигонов или каждые 30 секунд
                    current_time = time.time()
                    if count % 1000 == 0 or current_time - last_log_time > 30:
                        progress = count / total_estimated * 100
                        elapsed = current_time - start_time
                        logger.info(
                            f"Квадратные полигоны: {count}/{total_estimated} ({progress:.1f}%), пропущено: {skipped}, время: {elapsed:.1f} сек")
                        last_log_time = current_time

                        # Коммитим изменения каждые 1000 записей
                        self.connection.commit()

                except Error as e:
                    logger.error(f"Ошибка вставки квадратного полигона: {e}")
                    logger.error(f"Координаты: lat={rounded_lat}, lon={rounded_lon}")

                lon += lon_step
            lat += lat_step
            lat_index += 1

        self.connection.commit()
        logger.info(f"Создано {count} квадратных полигонов, пропущено {skipped}")
        return count

    def _generate_h3_hexagon_grid(self, area_km2: float):
        """Генерация шестиугольной сетки H3 для территории России"""
        cursor = self.connection.cursor()
        count = 0
        skipped = 0

        # Определяем разрешение H3 на основе площади
        resolution = self._get_h3_resolution(area_km2)
        logger.info(f"Используется разрешение H3: {resolution}")

        # Собираем все полигоны регионов России
        all_hexagons = set()

        for region in self.regions:
            try:
                region_polygon = json.loads(region['polygon'])

                # Создаем GeoJSON полигон в формате, ожидаемом H3
                geo_json_polygon = {
                    "type": "Polygon",
                    "coordinates": [[[coord[1], coord[0]] for coord in region_polygon[0]]]
                }

                # Получаем ячейки H3 для полигона региона
                hexagons = h3.polyfill(geo_json_polygon, resolution, geo_json_conformant=True)
                all_hexagons.update(hexagons)

                logger.info(f"Регион {region['id']}: получено {len(hexagons)} ячеек H3")

            except Exception as e:
                logger.error(f"Ошибка обработки региона {region['id']}: {e}")
                continue

        logger.info(f"Всего уникальных ячеек H3: {len(all_hexagons)}")

        # Вставляем ячейки в базу данных
        for h3_index in all_hexagons:
            try:
                boundary = h3.h3_to_geo_boundary(h3_index, geo_json=True)
                center_lat, center_lon = h3.h3_to_geo(h3_index)

                # Проверка на валидность и диапазон
                if center_lat is None or math.isnan(center_lat):
                    logger.error(f"Некорректная широта для ячейки {h3_index}: {center_lat}")
                    skipped += 1
                    continue
                if not (-90 <= center_lat <= 90):
                    logger.error(f"Широта {center_lat} для ячейки {h3_index} вне диапазона [-90, 90]")
                    skipped += 1
                    continue

                # Округление и проверка на превышение точности
                rounded_lat = self.round_coordinate(center_lat)
                rounded_lon = self.round_coordinate(center_lon)

                # Преобразование границ ячейки
                polygon_coords = [[lat, lng] for lng, lat in boundary]
                polygon_coords.append(polygon_coords[0])

                region_id = self.find_region_for_point(rounded_lat, rounded_lon)
                if not region_id:
                    skipped += 1
                    continue

                polygon_json = json.dumps([polygon_coords])

                cursor.execute("""
                    INSERT INTO grid_hexagon (polygon, center_lat, center_lon, area_km2, region_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (polygon_json, rounded_lat, rounded_lon, area_km2, region_id))
                count += 1
            except Exception as e:
                logger.error(f"Ошибка обработки ячейки {h3_index}: {e}")
                skipped += 1

        self.connection.commit()
        logger.info(f"Создано {count} ячеек H3, пропущено {skipped}")
        return count

    def _get_h3_resolution(self, area_km2: float) -> int:
        """Определяет разрешение H3 на основе целевой площади ячейки"""
        # Площади ячеек H3 для разных разрешений (в км²)
        resolutions = {
            0: 4250546.8477,
            1: 607220.978242,
            2: 86745.8540345,
            3: 12392.2648621,
            4: 1770.32355172,
            5: 252.903364532,
            6: 36.129052076,
            7: 5.16129315372,
            8: 0.737327593388,
            9: 0.105332513341,
            10: 0.0150475019059,
            11: 0.00214964312941,
            12: 0.00030709187563,
            13: 0.0000438702679471,
            14: 0.0000062671811353,
            15: 8.95311590757e-7
        }

        # Находим разрешение с наиболее близкой площадью
        best_res = 0
        min_diff = float('inf')

        for res, area in resolutions.items():
            diff = abs(area - area_km2)
            if diff < min_diff:
                min_diff = diff
                best_res = res

        return best_res

    def update_total_flights(self):
        """Обновление поля total_flights для всех полигонов с использованием Python для проверки"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Получаем все точки вылета из processed_flights
            logger.info("Загрузка точек вылета из processed_flights...")
            cursor.execute(
                "SELECT departure_lat, departure_lon FROM processed_flights WHERE departure_lat IS NOT NULL AND departure_lon IS NOT NULL")
            flight_points = cursor.fetchall()
            logger.info(f"Загружено {len(flight_points)} точек вылета")

            # Обновление для квадратных полигонов
            logger.info("Начинаем обновление total_flights для grid_square")
            cursor.execute("SELECT id, polygon FROM grid_square")
            square_polygons = cursor.fetchall()

            square_updates = []
            for poly in square_polygons:
                try:
                    polygon_coords = json.loads(poly['polygon'])[0]  # Берем первый полигон
                    count = 0

                    for point in flight_points:
                        if point['departure_lat'] and point['departure_lon']:
                            if self.is_point_in_polygon(point['departure_lat'], point['departure_lon'], polygon_coords):
                                count += 1

                    square_updates.append((count, poly['id']))

                    # Логируем прогресс каждые 100 полигонов
                    if len(square_updates) % 100 == 0:
                        logger.info(f"Обработано {len(square_updates)} квадратных полигонов")
                        # Пакетное обновление
                        update_cursor = self.connection.cursor()
                        update_cursor.executemany("UPDATE grid_square SET total_flights = %s WHERE id = %s",
                                                  square_updates)
                        self.connection.commit()
                        update_cursor.close()
                        square_updates = []

                except Exception as e:
                    logger.error(f"Ошибка обработки квадратного полигона {poly['id']}: {e}")
                    continue

            # Обновляем оставшиеся записи
            if square_updates:
                update_cursor = self.connection.cursor()
                update_cursor.executemany("UPDATE grid_square SET total_flights = %s WHERE id = %s", square_updates)
                self.connection.commit()
                update_cursor.close()

            logger.info("Обновление grid_square завершено")

            # Обновление для шестиугольных полигонов
            logger.info("Начинаем обновление total_flights для grid_hexagon")
            cursor.execute("SELECT id, polygon FROM grid_hexagon")
            hexagon_polygons = cursor.fetchall()

            hexagon_updates = []
            for poly in hexagon_polygons:
                try:
                    polygon_coords = json.loads(poly['polygon'])[0]  # Берем первый полигон
                    count = 0

                    for point in flight_points:
                        if point['departure_lat'] and point['departure_lon']:
                            if self.is_point_in_polygon(point['departure_lat'], point['departure_lon'], polygon_coords):
                                count += 1

                    hexagon_updates.append((count, poly['id']))

                    # Логируем прогресс каждые 100 полигонов
                    if len(hexagon_updates) % 100 == 0:
                        logger.info(f"Обработано {len(hexagon_updates)} шестиугольных полигонов")
                        # Пакетное обновление
                        update_cursor = self.connection.cursor()
                        update_cursor.executemany("UPDATE grid_hexagon SET total_flights = %s WHERE id = %s",
                                                  hexagon_updates)
                        self.connection.commit()
                        update_cursor.close()
                        hexagon_updates = []

                except Exception as e:
                    logger.error(f"Ошибка обработки шестиугольного полигона {poly['id']}: {e}")
                    continue

            # Обновляем оставшиеся записи
            if hexagon_updates:
                update_cursor = self.connection.cursor()
                update_cursor.executemany("UPDATE grid_hexagon SET total_flights = %s WHERE id = %s", hexagon_updates)
                self.connection.commit()
                update_cursor.close()

            self.connection.commit()
            logger.info("Обновление total_flights завершено")
            return True

        except Error as e:
            logger.error(f"Ошибка обновления total_flights: {e}")
            self.connection.rollback()
            return False

    def generate_grids(self, bbox: Tuple[float, float, float, float] = (41.0, 19.0, 82.0, 180.0)):
        """
        Генерация сеток полигонов для заданного bounding box
        bbox: (min_lat, min_lon, max_lat, max_lon)
        """
        if not self.connect():
            return False

        try:
            # Удаляем старые таблицы и создаем новые
            self.drop_grid_tables()
            self.create_settings_table()
            self.create_grid_tables()

            # Загружаем регионы России
            if not self.load_russia_regions():
                logger.error("Не удалось загрузить регионы России")
                return False

            # Получаем размер ячейки
            area_km2 = self.get_grid_cell_area()
            lat_step, lon_step = self.calculate_cell_size(area_km2)

            min_lat, min_lon, max_lat, max_lon = bbox

            logger.info(f"Начинаем генерацию сеток для области: {bbox}")
            logger.info(f"Размер ячейки: {area_km2} км²")
            logger.info(f"Шаг квадратной сетки: широта {lat_step:.6f}, долгота {lon_step:.6f}")

            # Генерируем квадратную сетку
            start_time = time.time()
            square_count = self._generate_square_grid(min_lat, min_lon, max_lat, max_lon, lat_step, lon_step, area_km2)
            square_time = time.time() - start_time

            # Генерируем шестиугольную сетку H3
            start_time = time.time()
            hexagon_count = self._generate_h3_hexagon_grid(area_km2)
            hexagon_time = time.time() - start_time

            # Обновляем количество полетов в полигонах
            start_time = time.time()
            self.update_total_flights()
            update_time = time.time() - start_time

            total_time = square_time + hexagon_time + update_time

            logger.info(f"Создано {square_count} квадратных полигонов за {square_time:.2f} сек")
            logger.info(f"Создано {hexagon_count} шестиугольных полигонов H3 за {hexagon_time:.2f} сек")
            logger.info(f"Обновление total_flights заняло {update_time:.2f} сек")
            logger.info(f"Общее время выполнения: {total_time:.2f} сек")

            return True

        except Error as e:
            logger.error(f"Ошибка генерации сеток: {e}")
            return False
        finally:
            if self.connection:
                self.connection.close()

    def update_grid_cell_area(self, new_area: float):
        """Обновление размера ячейки сетки в настройках"""
        if not self.connect():
            return False

        try:
            cursor = self.connection.cursor()

            # # Проверяем существование таблицы и столбца
            self.create_settings_table()

            cursor.execute("""
                UPDATE settings SET value = %s, updated_at = CURRENT_TIMESTAMP
                WHERE key_name = 'grid_cell_area'
            """, (str(new_area),))

            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO settings (key_name, value, description)
                    VALUES ('grid_cell_area', %s, 'Площадь ячейки сетки в км²')
                """, (str(new_area),))

            self.connection.commit()
            logger.info(f"Размер ячейки сетки обновлен: {new_area} км²")
            return True
        except Error as e:
            logger.error(f"Ошибка обновления размера ячейки: {e}")
            return False
        finally:
            if self.connection:
                self.connection.close()


# Пример использования
if __name__ == "__main__":
    generator = GridGenerator(DB_CONFIG)
    # Bounding box для России (примерные координаты)
    russia_bbox = (41.0, 19.0, 82.0, 180.0)

    # Можно обновить размер ячейки (необязательно)
    generator.update_grid_cell_area(7500)  # 10000 км²

    if generator.generate_grids(russia_bbox):
        logger.info("Сетки полигонов успешно созданы")
    else:
        logger.error("Ошибка при создании сеток")