# region_stats_updater.py
"""
Модуль формирования статистики по регионам.
Обновляет таблицу region_stats с расширенной статистикой полетов.
"""
import mysql.connector
from mysql.connector import Error
import logging
from datetime import date, timedelta
import time
from collections import defaultdict
import statistics
import settings
from decimal import Decimal

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../log.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class RegionStatsUpdaterFixed:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.region_areas = {}
        self.region_ids = {}

    def connect_to_db(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            logging.info("Успешное подключение к базе данных")
            return True
        except Error as e:
            logging.error(f"Ошибка подключения к MySQL: {e}")
            return False

    def close_connection(self):
        """Закрытие соединения с БД"""
        if self.connection:
            self.connection.close()
            logging.info("Соединение с базой данных закрыто")

    def check_table_exists(self, table_name: str) -> bool:
        """Проверка существования таблицы в базе данных"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() AND table_name = %s
            """, (table_name,))
            return cursor.fetchone()[0] == 1
        except Exception as e:
            logging.error(f"Ошибка проверки существования таблицы {table_name}: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def create_region_stats_table(self):
        """Создание таблицы region_stats с дополнительными полями"""
        try:
            cursor = self.connection.cursor()

            # Удаляем таблицу если существует
            if self.check_table_exists('region_stats'):
                cursor.execute("DROP TABLE IF EXISTS region_stats")

            cursor.execute("""
                CREATE TABLE region_stats (
                    region VARCHAR(100) NOT NULL,
                    region_id INT COMMENT 'ID региона из таблицы regions',
                    date DATE NOT NULL,
                    peak_load INT COMMENT 'Пиковая нагрузка: максимальное число полетов за час',
                    avg_daily_flights DECIMAL(10,2) COMMENT 'Среднее число полетов в сутки за месяц',
                    median_daily_flights DECIMAL(10,2) COMMENT 'Медианное число полетов в сутки за месяц',
                    monthly_change DECIMAL(10,2) COMMENT 'Процентное изменение числа полетов за месяц',
                    flight_density DECIMAL(15,6) COMMENT 'Число полетов на 1000 км² территории региона',
                    morning_flights INT COMMENT 'Количество полетов утром (06:00-12:00)',
                    afternoon_flights INT COMMENT 'Количество полетов днем (12:00-18:00)',
                    evening_flights INT COMMENT 'Количество полетов вечером (18:00-24:00)',
                    night_flights INT COMMENT 'Количество полетов ночью (00:00-06:00)',
                    total_flights INT COMMENT 'Общее количество полетов за день',
                    zero_days INT COMMENT 'Количество предыдущих дней без полетов (сбрасывается при наличии полетов)',
                    avg_duration_min INT COMMENT 'Средняя Длительность полета в минутах',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (region, date),
                    INDEX idx_region_date (region, date),
                    INDEX idx_date (date),
                    INDEX idx_region_id (region_id)
                ) COMMENT='Расширенная статистика полетов по регионам'
            """)
            self.connection.commit()
            logging.info("Таблица region_stats создана успешно")
        except Exception as e:
            logging.error(f"Ошибка создания таблицы region_stats: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def create_region_stats_month_table(self):
        """Создание таблицы region_stats_month для агрегированных данных по месяцам"""
        try:
            cursor = self.connection.cursor()

            # Удаляем таблицу если существует
            if self.check_table_exists('region_stats_month'):
                cursor.execute("DROP TABLE IF EXISTS region_stats_month")

            cursor.execute("""
                CREATE TABLE region_stats_month (
                    region VARCHAR(100) NOT NULL,
                    region_id INT COMMENT 'ID региона из таблицы regions',
                    month VARCHAR(7) NOT NULL COMMENT 'Год-месяц в формате YYYY-MM',
                    total_flights INT COMMENT 'Общее количество полетов за месяц',
                    avg_flight_duration DECIMAL(10,2) COMMENT 'Средняя длительность полета в минутах (игнорируя дни без полетов)',
                    peak_load INT COMMENT 'Максимальное количество полетов в день за месяц',
                    flight_density DECIMAL(15,6) COMMENT 'Плотность полетов на 1000 км² за месяц',
                    monthly_change DECIMAL(10,2) COMMENT 'Изменение числа полетов по сравнению с прошлым месяцем',
                    morning_flights INT COMMENT 'Количество утренних полетов за месяц',
                    afternoon_flights INT COMMENT 'Количество дневных полетов за месяц',
                    evening_flights INT COMMENT 'Количество вечерных полетов за месяц',
                    night_flights INT COMMENT 'Количество ночных полетов за месяц',
                    morning_percent DECIMAL(5,2) COMMENT 'Процент утренних полетов',
                    afternoon_percent DECIMAL(5,2) COMMENT 'Процент дневных полетов',
                    evening_percent DECIMAL(5,2) COMMENT 'Процент вечерных полетов',
                    night_percent DECIMAL(5,2) COMMENT 'Процент ночных полетов',
                    median_daily_flights DECIMAL(10,2) COMMENT 'Медианное число полетов в сутки за месяц',
                    zero_days INT COMMENT 'Максимальное количество дней без полетов в месяце',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (region, month),
                    INDEX idx_region_month (region, month),
                    INDEX idx_month (month),
                    INDEX idx_region_id (region_id)
                ) COMMENT='Агрегированная статистика полетов по регионам по месяцам'
            """)
            self.connection.commit()
            logging.info("Таблица region_stats_month создана успешно")
        except Exception as e:
            logging.error(f"Ошибка создания таблицы region_stats_month: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_region_areas_and_ids(self):
        """Получение площадей и ID регионов из базы данных"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, area_sq_km FROM regions")
            regions = cursor.fetchall()
            self.region_areas = {}
            self.region_ids = {}
            for region in regions:
                area = region['area_sq_km'] if region['area_sq_km'] and region['area_sq_km'] > 0 else 1
                self.region_areas[region['name']] = float(area)  # Преобразуем в float
                self.region_ids[region['name']] = region['id']
            logging.info(f"Получены данные для {len(self.region_areas)} регионов")
            return self.region_areas, self.region_ids
        except Exception as e:
            logging.error(f"Ошибка получения данных регионов: {e}")
            return {}, {}
        finally:
            if cursor:
                cursor.close()

    def get_all_regions(self):
        """Получение всех уникальных регионов из таблицы regions"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT name FROM regions")
            regions = [row['name'] for row in cursor.fetchall()]
            logging.info(f"Найдено {len(regions)} регионов в таблице regions")
            return regions
        except Exception as e:
            logging.error(f"Ошибка получения списка регионов: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_flights_data(self, start_date: date, end_date: date):
        """Получение всех данных о полетах за указанный период"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    COALESCE(departure_region, arrival_region) as region,
                    dof_date,
                    atd_time,
                    ata_time,
                    duration_min
                FROM processed_flights 
                WHERE dof_date BETWEEN %s AND %s
                AND (departure_region IS NOT NULL OR arrival_region IS NOT NULL)
            """, (start_date, end_date))
            flights = cursor.fetchall()
            logging.info(f"Получено {len(flights)} записей о полетах")
            return flights
        except Exception as e:
            logging.error(f"Ошибка получения данных о полетах: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def calculate_stats(self, flights_data, start_date: date, end_date: date):
        """Вычисление статистики на основе данных о полетах"""
        daily_stats = defaultdict(lambda: defaultdict(int))
        hourly_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        time_period_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        duration_stats = defaultdict(lambda: defaultdict(list))

        for flight in flights_data:
            region = flight['region']
            flight_date = flight['dof_date']
            atd_time = flight['atd_time']

            if not region or not flight_date:
                continue

            daily_stats[region][flight_date] += 1

            if atd_time:
                if isinstance(atd_time, timedelta):
                    total_seconds = atd_time.total_seconds()
                    hour = int(total_seconds // 3600) % 24
                else:
                    hour = atd_time.hour

                hourly_stats[region][flight_date][hour] += 1

                if 6 <= hour < 12:
                    time_period_stats[region][flight_date]['morning'] += 1
                elif 12 <= hour < 18:
                    time_period_stats[region][flight_date]['afternoon'] += 1
                elif 18 <= hour < 24:
                    time_period_stats[region][flight_date]['evening'] += 1
                else:
                    time_period_stats[region][flight_date]['night'] += 1

            if flight['duration_min']:
                duration_stats[region][flight_date].append(flight['duration_min'])

        return daily_stats, hourly_stats, time_period_stats, duration_stats

    def safe_calculate_flight_density(self, total_flights, area):
        """Безопасный расчет плотности полетов"""
        if area <= 0:
            return 0.0

        # Преобразуем total_flights к float если это Decimal
        if isinstance(total_flights, Decimal):
            total_flights = float(total_flights)

        density = (total_flights / area) * 1000
        max_density = 999999.999999
        if density > max_density:
            logging.warning(f"Плотность полетов превышает максимальное значение {max_density}: {density}")
            return max_density
        return round(density, 6)

    def populate_region_stats(self, start_date: date, end_date: date):
        """Заполнение таблицы region_stats расчетными данными с новым алгоритмом zero_days"""
        cursor = None
        try:
            start_time = time.time()
            cursor = self.connection.cursor()

            # Получаем все регионы
            all_regions = self.get_all_regions()
            if not all_regions:
                logging.warning("Не найдено регионов для обработки")
                return

            # Получаем данные о полетах
            flights_data = self.get_flights_data(start_date, end_date)
            daily_stats, hourly_stats, time_period_stats, duration_stats = self.calculate_stats(
                flights_data, start_date, end_date
            )

            self.get_region_areas_and_ids()
            batch_values = []

            # Словарь для отслеживания последовательных дней без полетов по регионам
            region_zero_days = defaultdict(int)

            # Обрабатываем каждый день в диапазоне
            current_date = start_date
            while current_date <= end_date:
                if current_date.day % 10 == 0:
                    logging.info(f"Обработка дата: {current_date}")

                for region in all_regions:
                    # Получаем статистику для текущего дня и региона
                    daily_count = daily_stats.get(region, {}).get(current_date, 0)

                    # Вычисляем количество полетов по времени суток
                    morning = time_period_stats.get(region, {}).get(current_date, {}).get('morning', 0)
                    afternoon = time_period_stats.get(region, {}).get(current_date, {}).get('afternoon', 0)
                    evening = time_period_stats.get(region, {}).get(current_date, {}).get('evening', 0)
                    night = time_period_stats.get(region, {}).get(current_date, {}).get('night', 0)

                    # Общее количество полетов за день
                    total_flights = morning + afternoon + evening + night

                    # Обновляем счетчик дней без полетов
                    if total_flights > 0:
                        region_zero_days[region] = 0  # Сбрасываем счетчик
                    else:
                        region_zero_days[region] += 1  # Увеличиваем счетчик

                    # Вычисляем среднюю длительность полетов
                    durations = duration_stats.get(region, {}).get(current_date, [])
                    avg_duration = int(statistics.mean(durations)) if durations else 0

                    # Пиковая нагрузка
                    peak_load = max(hourly_stats.get(region, {}).get(current_date, {}).values()) if hourly_stats.get(
                        region, {}).get(current_date, {}) else 0

                    # Плотность полетов
                    area = self.region_areas.get(region, 1)
                    flight_density = self.safe_calculate_flight_density(total_flights, area)

                    # Получаем ID региона
                    region_id = self.region_ids.get(region, None)

                    # Для остальных полей используем значения по умолчанию
                    # (эти поля будут обновляться в другом методе)
                    batch_values.append((
                        region,
                        region_id,
                        current_date,
                        peak_load,
                        0,  # avg_daily_flights
                        0,  # median_daily_flights
                        0,  # monthly_change
                        flight_density,
                        morning,
                        afternoon,
                        evening,
                        night,
                        total_flights,
                        region_zero_days[region],  # zero_days по новому алгоритму
                        avg_duration
                    ))

                current_date += timedelta(days=1)

                # Выполняем batch-вставку каждые 1000 записей
                if len(batch_values) >= 1000:
                    self.execute_batch_insert(cursor, batch_values, 'region_stats')
                    batch_values = []
                    self.connection.commit()

            # Вставляем оставшиеся записи
            if batch_values:
                self.execute_batch_insert(cursor, batch_values, 'region_stats')
                self.connection.commit()

            total_time = time.time() - start_time
            logging.info(f"Заполнение region_stats завершено за {total_time:.2f} секунд")

        except Exception as e:
            logging.error(f"Ошибка заполнения region_stats: {e}")
            self.connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def calculate_median_daily_flights(self):
        """Вычисление медианного числа полетов в сутки по месяцам"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Получаем все daily_flights по месяцам и регионам
            cursor.execute("""
                SELECT region, region_id, DATE_FORMAT(date, '%Y-%m') as month, total_flights
                FROM region_stats
                ORDER BY region, month, total_flights
            """)

            data = cursor.fetchall()

            # Группируем данные по региону и месяцу
            grouped_data = defaultdict(list)
            for row in data:
                key = (row['region'], row['region_id'], row['month'])
                grouped_data[key].append(row['total_flights'])

            # Вычисляем медиану для каждой группы
            median_results = {}
            for key, values in grouped_data.items():
                if values:
                    median_results[key] = statistics.median(values)
                else:
                    median_results[key] = 0

            return median_results

        except Exception as e:
            logging.error(f"Ошибка вычисления медианы: {e}")
            return {}
        finally:
            if cursor:
                cursor.close()

    def populate_region_stats_month(self):
        """Заполнение таблицы region_stats_month агрегированными данными"""
        cursor = None
        try:
            start_time = time.time()
            cursor = self.connection.cursor(dictionary=True)

            # Получаем агрегированные данные по месяцам (без медианы)
            cursor.execute("""
                SELECT 
                    region,
                    region_id,
                    DATE_FORMAT(date, '%Y-%m') as month,
                    SUM(total_flights) as total_flights,
                    AVG(CASE WHEN total_flights > 0 THEN avg_duration_min ELSE NULL END) as avg_flight_duration,
                    MAX(peak_load) as peak_load,
                    SUM(morning_flights) as morning_flights,
                    SUM(afternoon_flights) as afternoon_flights,
                    SUM(evening_flights) as evening_flights,
                    SUM(night_flights) as night_flights,
                    MAX(zero_days) as max_zero_days
                FROM region_stats
                GROUP BY region, region_id, DATE_FORMAT(date, '%Y-%m')
                ORDER BY region, month
            """)
            monthly_data = cursor.fetchall()

            # Вычисляем медиану daily_flights
            median_daily_flights = self.calculate_median_daily_flights()

            # Получаем площади регионов для расчета плотности
            self.get_region_areas_and_ids()

            # Вычисляем изменение по сравнению с предыдущим месяцем
            prev_month_data = {}
            batch_values = []

            for row in monthly_data:
                region = row['region']
                month = row['month']

                # Рассчитываем плотность полетов
                area = self.region_areas.get(region, 1)
                flight_density = self.safe_calculate_flight_density(row['total_flights'], area)

                # Вычисляем изменение по сравнению с предыдущим месяцем
                monthly_change = 0.0
                if region in prev_month_data:
                    prev_total = prev_month_data[region]
                    if prev_total > 0:
                        # Преобразуем Decimal к float для вычислений
                        current_total_float = float(row['total_flights'])
                        prev_total_float = float(prev_total)
                        monthly_change = ((current_total_float - prev_total_float) / prev_total_float) * 100
                    elif row['total_flights'] > 0:
                        monthly_change = 100.0

                # Сохраняем данные для следующего месяца
                prev_month_data[region] = row['total_flights']

                # Преобразуем среднюю длительность к float, если необходимо
                avg_duration = row['avg_flight_duration']
                if isinstance(avg_duration, Decimal):
                    avg_duration = float(avg_duration)

                # Рассчитываем проценты полетов по времени суток
                total = float(row['total_flights'])
                morning_percent = (float(row['morning_flights']) / total * 100) if total > 0 else 0
                afternoon_percent = (float(row['afternoon_flights']) / total * 100) if total > 0 else 0
                evening_percent = (float(row['evening_flights']) / total * 100) if total > 0 else 0
                night_percent = (float(row['night_flights']) / total * 100) if total > 0 else 0

                # Получаем медиану daily_flights
                median_key = (row['region'], row['region_id'], row['month'])
                median_daily = median_daily_flights.get(median_key, 0)

                batch_values.append((
                    region,
                    row['region_id'],
                    month,
                    int(row['total_flights']),  # Преобразуем к int
                    round(avg_duration or 0, 2),
                    row['peak_load'],
                    round(flight_density, 6),
                    round(monthly_change, 2),
                    row['morning_flights'],
                    row['afternoon_flights'],
                    row['evening_flights'],
                    row['night_flights'],
                    round(morning_percent, 2),
                    round(afternoon_percent, 2),
                    round(evening_percent, 2),
                    round(night_percent, 2),
                    round(median_daily, 2),
                    row['max_zero_days']
                ))

            # Выполняем вставку
            if batch_values:
                self.execute_batch_insert(cursor, batch_values, 'region_stats_month')
                self.connection.commit()

            total_time = time.time() - start_time
            logging.info(f"Заполнение region_stats_month завершено за {total_time:.2f} секунд")

        except Exception as e:
            logging.error(f"Ошибка заполнения region_stats_month: {e}")
            self.connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def execute_batch_insert(self, cursor, batch_values, table_name):
        """Выполнение batch-вставки данных"""
        try:
            if table_name == 'region_stats':
                cursor.executemany("""
                    INSERT INTO region_stats 
                    (region, region_id, date, peak_load, avg_daily_flights, median_daily_flights, 
                     monthly_change, flight_density, morning_flights, afternoon_flights, 
                     evening_flights, night_flights, total_flights, zero_days, avg_duration_min)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, batch_values)
            elif table_name == 'region_stats_month':
                cursor.executemany("""
                    INSERT INTO region_stats_month 
                    (region, region_id, month, total_flights, avg_flight_duration, peak_load,
                     flight_density, monthly_change, morning_flights, afternoon_flights,
                     evening_flights, night_flights, morning_percent, afternoon_percent,
                     evening_percent, night_percent, median_daily_flights, zero_days)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, batch_values)
        except Exception as e:
            logging.error(f"Ошибка при batch-вставке данных в {table_name}: {e}")
            for i, values in enumerate(batch_values[:5]):  # Логируем только первые 5 ошибок
                logging.error(f"Проблемные значения в строке {i}: {values}")
            raise

    def update_region_stats(self):
        """Основной метод для обновления статистики регионов"""
        try:
            if not self.connect_to_db():
                return False

            # Проверяем необходимые таблицы
            required_tables = ['processed_flights', 'regions']
            for table in required_tables:
                if not self.check_table_exists(table):
                    logging.error(f"Таблица {table} не существует")
                    return False

            # Создаем таблицы
            self.create_region_stats_table()
            self.create_region_stats_month_table()

            # Заполняем данными
            start_date = date(2024, 1, 1)
            end_date = date(2025, 7, 31)
            self.populate_region_stats(start_date, end_date)
            self.populate_region_stats_month()

            logging.info("Статистика регионов успешно обновлена")
            return True

        except Exception as e:
            logging.error(f"Ошибка при обновлении статистики регионов: {e}")
            return False
        finally:
            self.close_connection()


def update_region_stats_main():
    """Функция для отдельного запуска обновления статистики"""
    logging.info("Запуск обновления статистики регионов (исправленная версия)")
    updater = RegionStatsUpdaterFixed(settings.DB_CONFIG)
    success = updater.update_region_stats()
    if success:
        logging.info("Обновление статистики регионов завершено успешно")
    else:
        logging.error("Обновление статистики регионов завершено с ошибками")
    return success


if __name__ == "__main__":
    update_region_stats_main()