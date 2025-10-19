# generate_area_bpla.py
"""
Модуль генерации площадок для беспилотных авиационных систем (БАС).

В рамках национального проекта «Беспилотные авиационные системы» (2024-2030)
предусматривается создание 290 посадочных площадок для БПЛА на территории России.

Алгоритм размещения площадок основывается на:
1. Анализе трафика полетов в гексагональной сетке
2. Исключении запретных зон для полетов
3. Оптимизации покрытия территории с учетом региональной специфики

Автор: AI Assistant
Дата: 2025
"""

import mysql.connector
from mysql.connector import Error
import logging
from typing import List, Tuple, Optional, Dict
import json
import math
from datetime import datetime
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import sys
import os

# Настройка логирования
logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class AreaBPLAGenerator:
    """
    Генератор площадок для беспилотных авиационных систем.
    
    Основные функции:
    - Анализ трафика полетов БПЛА по гексагональной сетке
    - Исключение запретных зон полетов
    - Расчет оптимального размещения площадок
    - Сохранение результатов в базу данных
    """
    
    # Константы для расчета рейтинга
    TRAFFIC_WEIGHT = 0.4          # Вес трафика в расчете рейтинга (40%)
    NO_FLY_ZONE_PENALTY = -10000  # Штраф за нахождение в запретной зоне
    MIN_DISTANCE_KM = 50          # Минимальное расстояние между площадками (км)
    RADIUS_SEARCH_KM = 100        # Радиус поиска ближайших гексагонов (км)
    
    # Региональные квоты
    MIN_SITES_PER_REGION = 1      # Минимум площадок на регион (если есть трафик > 50)
    MAX_SITES_PER_REGION = 15     # Максимум площадок на один регион
    
    # Бонусы и штрафы
    FIRST_SITE_BONUS = 1000       # Бонус за первую площадку в регионе
    COVERAGE_BONUS = 500          # Бонус если в регионе < 3 площадок
    OVERCROWDING_PENALTY = -800   # Штраф если в регионе > 10 площадок
    AIRPORT_BONUS = 300           # Бонус за близость к аэропорту (10-30 км)
    
    def __init__(self, db_config: Dict):
        """
        Инициализация генератора.
        
        Args:
            db_config: Словарь с параметрами подключения к БД
        """
        self.db_config = db_config
        self.connection = None
        self.default_count = 290  # Количество площадок по умолчанию
        
    def connect(self) -> bool:
        """Установка соединения с базой данных."""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            return True
        except Error as e:
            print(f"Ошибка подключения к БД: {e}")
            return False
    
    def disconnect(self):
        """Закрытие соединения с базой данных."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def check_table_exists(self, table_name: str) -> bool:
        """
        Проверяет существование таблицы.
        
        Args:
            table_name: Название таблицы
            
        Returns:
            True если таблица существует
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone() is not None
            cursor.close()
            return result
        except Error as e:
            logger.error(f"Ошибка проверки таблицы {table_name}: {e}")
            return False
    
    def create_area_bpla_table(self):
        """Создание таблицы area_bpla для хранения площадок."""
        try:
            cursor = self.connection.cursor()
            
            # Удаляем таблицу если существует
            if self.check_table_exists('area_bpla'):
                cursor.execute("DROP TABLE area_bpla")
            
            # Создаем новую таблицу
            cursor.execute("""
                CREATE TABLE area_bpla (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Номер площадки',
                    center_lat DECIMAL(11, 8) NOT NULL COMMENT 'Широта центра площадки',
                    center_lon DECIMAL(11, 8) NOT NULL COMMENT 'Долгота центра площадки',
                    total_flights INT DEFAULT 0 COMMENT 'Число полётов в ближайших гексагонах',
                    hexagon_id INT COMMENT 'ID ближайшего гексагона',
                    rating FLOAT NOT NULL COMMENT 'Рейтинг площадки (выше = лучше)',
                    region_id INT COMMENT 'Идентификатор региона',
                    year INT COMMENT 'Год ввода в эксплуатацию (2026-2030)',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата создания записи',
                    
                    INDEX idx_rating (rating),
                    INDEX idx_region_id (region_id),
                    INDEX idx_hexagon_id (hexagon_id),
                    INDEX idx_center (center_lat, center_lon),
                    INDEX idx_year (year)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 
                COMMENT='Площадки для беспилотных авиационных систем (БАС)'
            """)
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"❌ Ошибка создания таблицы area_bpla: {e}")
            return False
    
    def get_target_count(self) -> int:
        """
        Получение целевого количества площадок из таблицы settings.
        
        Returns:
            Количество площадок (по умолчанию 290)
        """
        try:
            cursor = self.connection.cursor()
            
            # Проверяем существование таблицы settings
            if not self.check_table_exists('settings'):
                return self.default_count
            
            # Пытаемся получить значение
            cursor.execute("""
                SELECT value FROM settings 
                WHERE key_name = 'count_area_bpla'
            """)
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                count = int(result[0])
                return count
            else:
                # Если записи нет, создаем её
                cursor = self.connection.cursor()
                cursor.execute("""
                    INSERT INTO settings (key_name, value, description)
                    VALUES ('count_area_bpla', %s, 'Целевое количество площадок для БПЛА')
                    ON DUPLICATE KEY UPDATE value = value
                """, (str(self.default_count),))
                self.connection.commit()
                cursor.close()
                return self.default_count
                
        except Error as e:
            logger.error(f"❌ Ошибка получения целевого количества: {e}")
            return self.default_count
    
    def get_hexagons_with_traffic(self) -> List[Dict]:
        """
        Получение всех гексагонов с информацией о трафике.
        
        Returns:
            Список словарей с данными гексагонов
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    id,
                    center_lat,
                    center_lon,
                    total_flights,
                    region_id,
                    polygon
                FROM grid_hexagon
                WHERE total_flights > 0
                ORDER BY total_flights DESC
            """)
            
            hexagons = cursor.fetchall()
            cursor.close()
            return hexagons
            
        except Error as e:
            logger.error(f"❌ Ошибка получения гексагонов: {e}")
            return []
    
    def get_airports(self) -> List[Dict]:
        """
        Получение координат аэропортов и аэродромов из таблицы points.
        
        Returns:
            Список словарей с координатами аэропортов
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Ищем аэропорты по ключевым словам в названии
            cursor.execute("""
                SELECT id, name, polygon
                FROM points
                WHERE (LOWER(name) LIKE '%аэропорт%' 
                   OR LOWER(name) LIKE '%аэродром%'
                   OR LOWER(name) LIKE '%airport%')
                AND isActive = 1
            """)
            
            airports_data = cursor.fetchall()
            cursor.close()
            
            airports = []
            for airport in airports_data:
                try:
                    # Парсим полигон и берем центр
                    polygon_data = json.loads(airport['polygon'])
                    if isinstance(polygon_data, list) and len(polygon_data) > 0:
                        coords = polygon_data[0]
                        if len(coords) > 0:
                            # Вычисляем центр полигона
                            avg_lat = sum(c[0] for c in coords) / len(coords)
                            avg_lon = sum(c[1] for c in coords) / len(coords)
                            airports.append({
                                'id': airport['id'],
                                'name': airport['name'],
                                'lat': avg_lat,
                                'lon': avg_lon
                            })
                except Exception:
                    continue
            
            return airports
            
        except Error as e:
            return []
    
    def get_no_fly_zones(self) -> List[Polygon]:
        """
        Получение запретных зон для полетов из таблицы points.
        
        Ищет полигоны с признаком запрета для БПЛА.
        В будущем это может быть JOIN с points_type где no_bpla=1.
        Пока используем все активные ограничения из points.
        
        Returns:
            Список полигонов Shapely с запретными зонами
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Получаем все активные ограничения
            # TODO: Добавить фильтрацию по points_type.no_bpla = 1 когда таблица будет создана
            cursor.execute("""
                SELECT polygon
                FROM points
                WHERE isActive = 1
            """)
            
            zones = cursor.fetchall()
            cursor.close()
            
            no_fly_polygons = []
            for zone in zones:
                try:
                    # Парсим полигон из строки
                    polygon_data = json.loads(zone['polygon'])
                    if isinstance(polygon_data, list) and len(polygon_data) > 0:
                        # Создаем Shapely полигон
                        coords = [(float(lat), float(lon)) for lat, lon in polygon_data]
                        if len(coords) >= 3:
                            poly = Polygon(coords)
                            no_fly_polygons.append(poly)
                except Exception as e:
                    pass
                    continue
            
            return no_fly_polygons
            
        except Error as e:
            logger.error(f"❌ Ошибка получения запретных зон: {e}")
            return []
    
    def calculate_distance_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Расчет расстояния между двумя точками по формуле гаверсинуса.
        
        Args:
            lat1, lon1: Координаты первой точки
            lat2, lon2: Координаты второй точки
            
        Returns:
            Расстояние в километрах
        """
        R = 6371  # Радиус Земли в км
        
        lat1_rad = math.radians(float(lat1))
        lat2_rad = math.radians(float(lat2))
        delta_lat = math.radians(float(lat2) - float(lat1))
        delta_lon = math.radians(float(lon2) - float(lon1))
        
        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * \
            math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def is_point_in_no_fly_zone(self, lat: float, lon: float, no_fly_zones: List[Polygon]) -> bool:
        """
        Проверяет, находится ли точка в запретной зоне.
        
        Args:
            lat, lon: Координаты точки
            no_fly_zones: Список запретных зон
            
        Returns:
            True если точка в запретной зоне
        """
        point = Point(float(lat), float(lon))
        
        for zone in no_fly_zones:
            try:
                if zone.contains(point):
                    return True
            except Exception:
                continue
        
        return False
    
    def calculate_nearby_traffic(self, lat: float, lon: float, hexagons: List[Dict]) -> int:
        """
        Расчет суммарного трафика в ближайших гексагонах.
        
        Args:
            lat, lon: Координаты площадки
            hexagons: Список всех гексагонов
            
        Returns:
            Суммарный трафик в радиусе RADIUS_SEARCH_KM
        """
        total_traffic = 0
        
        for hexagon in hexagons:
            distance = self.calculate_distance_km(
                lat, lon,
                hexagon['center_lat'], hexagon['center_lon']
            )
            
            if distance <= self.RADIUS_SEARCH_KM:
                # Трафик взвешивается обратно пропорционально расстоянию
                weight = 1 / (1 + distance / 10)  # Нормализация
                total_traffic += int(hexagon['total_flights'] * weight)
        
        return total_traffic
    
    def check_airport_proximity(self, lat: float, lon: float, airports: List[Dict]) -> float:
        """
        Проверка близости к аэропортам и расчет бонуса.
        
        Оптимальное расстояние: 10-30 км от аэропорта.
        
        Args:
            lat, lon: Координаты площадки
            airports: Список аэропортов
            
        Returns:
            Бонус за близость к аэропорту
        """
        if not airports:
            return 0
        
        min_distance = float('inf')
        for airport in airports:
            distance = self.calculate_distance_km(lat, lon, airport['lat'], airport['lon'])
            if distance < min_distance:
                min_distance = distance
        
        # Оптимальная зона: 10-30 км
        if 10 <= min_distance <= 30:
            return self.AIRPORT_BONUS
        # Приемлемая зона: 5-50 км
        elif 5 <= min_distance <= 50:
            return self.AIRPORT_BONUS * 0.5
        # Слишком близко (< 5 км) или слишком далеко (> 50 км)
        else:
            return 0
    
    def count_sites_by_region(self, existing_sites: List[Dict]) -> Dict[int, int]:
        """
        Подсчет количества площадок по регионам.
        
        Args:
            existing_sites: Список уже размещенных площадок
            
        Returns:
            Словарь {region_id: количество_площадок}
        """
        region_counts = {}
        for site in existing_sites:
            region_id = site.get('region_id')
            if region_id:
                region_counts[region_id] = region_counts.get(region_id, 0) + 1
        return region_counts
    
    def calculate_rating(self, lat: float, lon: float, hexagons: List[Dict], 
                        no_fly_zones: List[Polygon], existing_sites: List[Dict],
                        airports: List[Dict], region_id: int) -> float:
        """
        Улучшенный расчет рейтинга для потенциальной площадки.
        
        Учитывает:
        - Трафик БПЛА (40%)
        - Региональные квоты (30%)
        - Близость к аэропортам (10%)
        - Равномерность распределения (20%)
        
        Args:
            lat, lon: Координаты потенциальной площадки
            hexagons: Список гексагонов с трафиком
            no_fly_zones: Список запретных зон
            existing_sites: Список уже размещенных площадок
            airports: Список аэропортов
            region_id: ID региона
            
        Returns:
            Рейтинг площадки (выше = лучше)
        """
        # Проверка на запретную зону
        if self.is_point_in_no_fly_zone(lat, lon, no_fly_zones):
            return self.NO_FLY_ZONE_PENALTY
        
        # Проверка минимального расстояния до существующих площадок
        for site in existing_sites:
            distance = self.calculate_distance_km(lat, lon, site['lat'], site['lon'])
            if distance < self.MIN_DISTANCE_KM:
                return -5000
        
        # 1. ТРАФИК БПЛА (40%)
        nearby_traffic = self.calculate_nearby_traffic(lat, lon, hexagons)
        traffic_score = nearby_traffic * self.TRAFFIC_WEIGHT
        
        # 2. РЕГИОНАЛЬНЫЕ КВОТЫ (30%)
        region_counts = self.count_sites_by_region(existing_sites)
        sites_in_region = region_counts.get(region_id, 0)
        
        if sites_in_region == 0:
            region_bonus = self.FIRST_SITE_BONUS  # Первая площадка в регионе
        elif sites_in_region < 3:
            region_bonus = self.COVERAGE_BONUS     # Нужно больше покрытия
        elif sites_in_region >= self.MAX_SITES_PER_REGION:
            return -8000  # Превышен лимит для региона
        elif sites_in_region > 10:
            region_bonus = self.OVERCROWDING_PENALTY  # Слишком много
        else:
            region_bonus = 0
        
        # 3. БЛИЗОСТЬ К АЭРОПОРТАМ (10%)
        airport_bonus = self.check_airport_proximity(lat, lon, airports)
        
        # 4. РАВНОМЕРНОСТЬ (20%)
        # Бонус за покрытие регионов с малым количеством площадок
        total_regions_with_sites = len(region_counts)
        if total_regions_with_sites > 0:
            avg_sites_per_region = len(existing_sites) / total_regions_with_sites
            if sites_in_region < avg_sites_per_region:
                uniformity_bonus = 300  # Регион недопокрыт
            else:
                uniformity_bonus = 0
        else:
            uniformity_bonus = 0
        
        # ИТОГОВЫЙ РЕЙТИНГ
        rating = (
            traffic_score +        # 40%
            region_bonus +         # 30%
            airport_bonus +        # 10%
            uniformity_bonus       # 20%
        )
        
        return rating
    
    def find_nearest_hexagon(self, lat: float, lon: float, hexagons: List[Dict]) -> Optional[int]:
        """
        Находит ближайший гексагон к заданной точке.
        
        Args:
            lat, lon: Координаты точки
            hexagons: Список гексагонов
            
        Returns:
            ID ближайшего гексагона или None
        """
        if not hexagons:
            return None
        
        min_distance = float('inf')
        nearest_id = None
        
        for hexagon in hexagons:
            distance = self.calculate_distance_km(
                lat, lon,
                hexagon['center_lat'], hexagon['center_lon']
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_id = hexagon['id']
        
        return nearest_id
    
    def generate_sites(self, target_count: int) -> bool:
        """
        Генерация площадок для БПЛА.
        
        Алгоритм:
        1. Получить все гексагоны с трафиком
        2. Получить запретные зоны
        3. Для каждого гексагона рассчитать рейтинг с учетом:
           - Трафика в окрестности
           - Отсутствия запретных зон
           - Минимального расстояния между площадками
        4. Выбрать топ N мест по рейтингу
        5. Сохранить в базу данных
        
        Args:
            target_count: Количество площадок для создания
            
        Returns:
            True если генерация успешна
        """
        try:
            print(f"Генерация {target_count} площадок (улучшенный алгоритм)...")
            
            # Получаем данные
            hexagons = self.get_hexagons_with_traffic()
            if not hexagons:
                print("Ошибка: не найдено гексагонов с трафиком")
                return False
            
            no_fly_zones = self.get_no_fly_zones()
            airports = self.get_airports()
            print(f"  Загружено аэропортов: {len(airports)}")
            
            # Список для хранения кандидатов
            candidates = []
            existing_sites = []  # Список уже выбранных площадок
            
            # Проходим по гексагонам и рассчитываем рейтинги
            total_hexagons = len(hexagons)
            for idx, hexagon in enumerate(hexagons):
                lat = float(hexagon['center_lat'])
                lon = float(hexagon['center_lon'])
                region_id = hexagon['region_id']
                
                # Рассчитываем рейтинг с улучшенным алгоритмом
                rating = self.calculate_rating(
                    lat, lon, hexagons, no_fly_zones, 
                    existing_sites, airports, region_id
                )
                
                # Добавляем в список кандидатов если рейтинг положительный
                if rating > 0:
                    candidates.append({
                        'lat': lat,
                        'lon': lon,
                        'rating': rating,
                        'total_flights': self.calculate_nearby_traffic(lat, lon, hexagons),
                        'hexagon_id': hexagon['id'],
                        'region_id': region_id
                    })
            
            # Сортируем по рейтингу (от большего к меньшему)
            candidates.sort(key=lambda x: x['rating'], reverse=True)
            
            # Выбираем площадки с учетом региональных квот
            selected_sites = []
            region_counts = {}
            
            for candidate in candidates:
                if len(selected_sites) >= target_count:
                    break
                
                region_id = candidate['region_id']
                
                # Проверяем региональный лимит
                if region_counts.get(region_id, 0) >= self.MAX_SITES_PER_REGION:
                    continue
                
                # Проверяем минимальное расстояние до уже выбранных
                too_close = False
                for site in selected_sites:
                    distance = self.calculate_distance_km(
                        candidate['lat'], candidate['lon'],
                        site['lat'], site['lon']
                    )
                    if distance < self.MIN_DISTANCE_KM:
                        too_close = True
                        break
                
                if not too_close:
                    selected_sites.append(candidate)
                    region_counts[region_id] = region_counts.get(region_id, 0) + 1
            
            # Распределяем площадки по годам (2026-2030) с учетом рейтинга
            # Площадки с высоким рейтингом получают ранние годы
            years = [2026, 2027, 2028, 2029, 2030]
            sites_per_year = len(selected_sites) / len(years)
            
            for idx, site in enumerate(selected_sites):
                # Определяем год на основе индекса (лучшие → 2026, худшие → 2030)
                year_index = min(int(idx / sites_per_year), len(years) - 1)
                site['year'] = years[year_index]
            
            # Сохраняем в базу данных
            cursor = self.connection.cursor()
            
            for site in selected_sites:
                cursor.execute("""
                    INSERT INTO area_bpla 
                    (center_lat, center_lon, total_flights, hexagon_id, rating, region_id, year)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    site['lat'],
                    site['lon'],
                    site['total_flights'],
                    site['hexagon_id'],
                    site['rating'],
                    site['region_id'],
                    site['year']
                ))
            
            self.connection.commit()
            cursor.close()
            
            # Расширенная статистика
            print(f"\n{'='*60}")
            print(f"РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ (улучшенный алгоритм)")
            print(f"{'='*60}")
            print(f"Создано площадок: {len(selected_sites)}")
            
            if selected_sites:
                total_flights = sum(s['total_flights'] for s in selected_sites)
                avg_rating = sum(s['rating'] for s in selected_sites) / len(selected_sites)
                covered_regions = len(set(s.get('region_id') for s in selected_sites if s.get('region_id')))
                
                print(f"Общий трафик: {total_flights} полетов")
                print(f"Средний рейтинг: {avg_rating:.2f}")
                print(f"Охвачено регионов: {covered_regions}")
                
                # Статистика по годам
                print(f"\nРаспределение по годам:")
                year_stats = {}
                for site in selected_sites:
                    year = site['year']
                    year_stats[year] = year_stats.get(year, 0) + 1
                for year in sorted(year_stats.keys()):
                    print(f"  {year}: {year_stats[year]} площадок")
                
                # Региональное распределение (топ-10)
                print(f"\nТоп-10 регионов по количеству площадок:")
                region_stats = {}
                for site in selected_sites:
                    rid = site.get('region_id')
                    if rid:
                        region_stats[rid] = region_stats.get(rid, 0) + 1
                
                sorted_regions = sorted(region_stats.items(), key=lambda x: x[1], reverse=True)
                for idx, (region_id, count) in enumerate(sorted_regions[:10], 1):
                    print(f"  {idx}. Регион {region_id}: {count} площадок")
                
                # Проверка региональных квот
                max_in_region = max(region_stats.values()) if region_stats else 0
                min_in_region = min(region_stats.values()) if region_stats else 0
                print(f"\nРегиональный баланс:")
                print(f"  Макс. площадок в регионе: {max_in_region}")
                print(f"  Мин. площадок в регионе: {min_in_region}")
                print(f"  Среднее по регионам: {len(selected_sites) / covered_regions:.1f}")
            
            print(f"{'='*60}")
            
            return True
            
        except Exception as e:
            print(f"Ошибка генерации: {e}")
            return False
    
    
    def run(self):
        """
        Основной метод запуска генерации площадок.
        
        Выполняет полный цикл:
        1. Подключение к БД
        2. Создание таблицы
        3. Получение параметров
        4. Генерация площадок
        5. Отключение от БД
        """
        try:
            # Подключение
            if not self.connect():
                return False
            
            # Создание таблицы
            if not self.create_area_bpla_table():
                return False
            
            # Получение целевого количества
            target_count = self.get_target_count()
            
            # Генерация площадок
            success = self.generate_sites(target_count)
            
            return success
            
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            return False
        finally:
            self.disconnect()


def main():
    """Точка входа для запуска модуля."""
    # Импортируем настройки
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from settings import DB_CONFIG
    
    # Создаем генератор
    generator = AreaBPLAGenerator(DB_CONFIG)
    
    # Запускаем генерацию
    if generator.run():
        print("\nГотово!")
    else:
        print("\nОшибка при генерации")


if __name__ == "__main__":
    main()

