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
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        self.region_areas = {}  # region_id -> area
        self.region_names = {}  # region_id -> name

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
CREATE TABLE `region_stats` (
  `region_id` int(11) NOT NULL COMMENT 'ID региона из таблицы regions',
  `region` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Название региона (для удобства, не используется в логике)',
  `date` date NOT NULL,
  `prediction` enum('download','prediction') NOT NULL DEFAULT 'download' COMMENT 'Тип полетов: download - настоящие, prediction - прогнозные',
  `peak_load` int(11) DEFAULT NULL COMMENT 'Пиковая нагрузка: максимальное число полетов за час',
  `avg_daily_flights` double DEFAULT NULL COMMENT 'Среднее число полетов в сутки за месяц',
  `median_daily_flights` double DEFAULT NULL COMMENT 'Медианное число полетов в сутки за месяц',
  `monthly_change` double DEFAULT NULL COMMENT 'Процентное изменение числа полетов за месяц',
  `flight_density` double DEFAULT NULL COMMENT 'Число полетов на 1000 км² территории региона',
  `morning_flights` int(11) DEFAULT NULL COMMENT 'Количество полетов утром (06:00-12:00)',
  `afternoon_flights` int(11) DEFAULT NULL COMMENT 'Количество полетов днем (12:00-18:00)',
  `evening_flights` int(11) DEFAULT NULL COMMENT 'Количество полетов вечером (18:00-24:00)',
  `night_flights` int(11) DEFAULT NULL COMMENT 'Количество полетов ночью (00:00-06:00)',
  `total_flights` int(11) DEFAULT NULL COMMENT 'Общее количество полетов за день',
  `zero_days` int(11) DEFAULT NULL COMMENT 'Количество предыдущих дней без полетов (сбрасывается при наличии полетов)',
  `avg_duration_min` int(11) DEFAULT NULL COMMENT 'Средняя Длительность полета в минутах',
  `eet_info` double DEFAULT NULL COMMENT 'Среднее расчетное время полета в минутах',
  `quantity` double DEFAULT NULL COMMENT 'Среднее количество БПЛА',
  `altitude_info` double DEFAULT NULL COMMENT 'Средняя высота полета в метрах',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`region_id`,`date`,`prediction`),
  KEY `idx_region_id_date` (`region_id`,`date`),
  KEY `idx_date` (`date`),
  KEY `idx_prediction` (`prediction`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Расширенная статистика полетов по регионам';
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
                CREATE TABLE `region_stats_month` (
  `region_id` int(11) NOT NULL COMMENT 'ID региона из таблицы regions',
  `region` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Название региона (для удобства, не используется в логике)',
  `month` varchar(7) NOT NULL COMMENT 'Год-месяц в формате YYYY-MM',
  `prediction` enum('download','prediction') NOT NULL DEFAULT 'download' COMMENT 'Тип полетов: download - настоящие, prediction - прогнозные',
  `total_flights` int(11) DEFAULT NULL COMMENT 'Общее количество полетов за месяц',
  `avg_flight_duration` double DEFAULT NULL COMMENT 'Средняя длительность полета в минутах (игнорируя дни без полетов)',
  `peak_load` int(11) DEFAULT NULL COMMENT 'Максимальное количество полетов в день за месяц',
  `flight_density` double DEFAULT NULL COMMENT 'Плотность полетов на 1000 км² за месяц',
  `monthly_change` double DEFAULT NULL COMMENT 'Изменение числа полетов по сравнению с прошлым месяцем',
  `morning_flights` int(11) DEFAULT NULL COMMENT 'Количество утренних полетов за месяц',
  `afternoon_flights` int(11) DEFAULT NULL COMMENT 'Количество дневных полетов за месяц',
  `evening_flights` int(11) DEFAULT NULL COMMENT 'Количество вечерных полетов за месяц',
  `night_flights` int(11) DEFAULT NULL COMMENT 'Количество ночных полетов за месяц',
  `morning_percent` double DEFAULT NULL COMMENT 'Процент утренних полетов',
  `afternoon_percent` double DEFAULT NULL COMMENT 'Процент дневных полетов',
  `evening_percent` double DEFAULT NULL COMMENT 'Процент вечерных полетов',
  `night_percent` double DEFAULT NULL COMMENT 'Процент ночных полетов',
  `median_daily_flights` double DEFAULT NULL COMMENT 'Медианное число полетов в сутки за месяц',
  `zero_days` int(11) DEFAULT NULL COMMENT 'Максимальное количество дней без полетов в месяце',
  `eet_info` double DEFAULT NULL COMMENT 'Среднее расчетное время полета в минутах',
  `quantity` double DEFAULT NULL COMMENT 'Среднее количество БПЛА',
  `altitude_info` double DEFAULT NULL COMMENT 'Средняя высота полета в метрах',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`region_id`,`month`,`prediction`),
  KEY `idx_region_id_month` (`region_id`,`month`),
  KEY `idx_month` (`month`),
  KEY `idx_prediction` (`prediction`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Агрегированная статистика полетов по регионам по месяцам';
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
        """Получение площадей и названий регионов из базы данных по ID"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, area_sq_km FROM regions")
            regions = cursor.fetchall()
            self.region_areas = {}
            self.region_names = {}
            for region in regions:
                region_id = region['id']
                area = region['area_sq_km'] if region['area_sq_km'] and region['area_sq_km'] > 0 else 1
                self.region_areas[region_id] = float(area)  # Преобразуем в float
                self.region_names[region_id] = region['name']
            logging.info(f"Получены данные для {len(self.region_areas)} регионов")
            return self.region_areas, self.region_names
        except Exception as e:
            logging.error(f"Ошибка получения данных регионов: {e}")
            return {}, {}
        finally:
            if cursor:
                cursor.close()

    def get_all_regions(self):
        """Получение всех ID регионов из таблицы regions"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id FROM regions")
            region_ids = [row['id'] for row in cursor.fetchall()]
            logging.info(f"Найдено {len(region_ids)} регионов в таблице regions")
            return region_ids
        except Exception as e:
            logging.error(f"Ошибка получения списка регионов: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_setting_value(self, key_name: str, default_value: str = None) -> str:
        """Получение значения настройки из таблицы settings"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT value FROM settings WHERE key_name = %s", (key_name,))
            result = cursor.fetchone()
            return result['value'] if result else default_value
        except Exception as e:
            logging.error(f"Ошибка получения настройки {key_name}: {e}")
            return default_value
        finally:
            if cursor:
                cursor.close()

    def get_flights_data(self, start_date: date, end_date: date):
        """Получение всех данных о полетах за указанный период с использованием region_id"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Сначала проверим общее количество записей
            cursor.execute("SELECT COUNT(*) as total FROM processed_flights")
            total_count = cursor.fetchone()['total']
            logging.info(f"Всего записей в processed_flights: {total_count}")
            
            # Проверим записи с регионами
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM processed_flights 
                WHERE region_id > 0
            """)
            with_regions = cursor.fetchone()['count']
            logging.info(f"Записей с region_id: {with_regions}")
            
            # Основной запрос - используем region_id и получаем название региона через JOIN
            cursor.execute("""
                SELECT 
                    pf.region_id,
                    r.name as region_name,
                    pf.dof_date,
                    pf.atd_time,
                    pf.ata_time,
                    pf.duration_min,
                    pf.prediction,
                    pf.eet_info,
                    pf.quantity,
                    pf.altitude_max as altitude
                FROM processed_flights pf
                LEFT JOIN regions r ON pf.region_id = r.id
                WHERE pf.dof_date BETWEEN %s AND %s
                AND pf.region_id > 0
            """, (start_date, end_date))
            flights = cursor.fetchall()
            logging.info(f"Получено {len(flights)} записей о полетах за период {start_date} - {end_date}")
            
            # Покажем несколько примеров для отладки
            if flights:
                logging.info("Примеры записей:")
                for i, flight in enumerate(flights[:3]):
                    logging.info(f"  {i+1}: region_id={flight['region_id']}, region={flight['region_name']}, date={flight['dof_date']}, prediction={flight['prediction']}")
            
            return flights
        except Exception as e:
            logging.error(f"Ошибка получения данных о полетах: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def calculate_stats(self, flights_data, start_date: date, end_date: date):
        """Вычисление статистики на основе данных о полетах (по region_id)"""
        daily_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        hourly_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
        time_period_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
        duration_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        eet_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        quantity_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        altitude_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for flight in flights_data:
            region_id = flight['region_id']
            flight_date = flight['dof_date']
            atd_time = flight['atd_time']
            prediction = flight.get('prediction')
            
            # Обрабатываем prediction: если None или пустая строка, используем 'download'
            if not prediction or prediction == '':
                prediction = 'download'
            elif prediction not in ['download', 'prediction']:
                # Если значение не соответствует ожидаемым, логируем и используем 'download'
                logging.warning(f"Неожиданное значение prediction: '{prediction}', используем 'download'")
                prediction = 'download'

            if not region_id or not flight_date:
                continue

            daily_stats[region_id][prediction][flight_date] += 1

            if atd_time:
                if isinstance(atd_time, timedelta):
                    total_seconds = atd_time.total_seconds()
                    hour = int(total_seconds // 3600) % 24
                else:
                    hour = atd_time.hour

                hourly_stats[region_id][prediction][flight_date][hour] += 1

                if 6 <= hour < 12:
                    time_period_stats[region_id][prediction][flight_date]['morning'] += 1
                elif 12 <= hour < 18:
                    time_period_stats[region_id][prediction][flight_date]['afternoon'] += 1
                elif 18 <= hour < 24:
                    time_period_stats[region_id][prediction][flight_date]['evening'] += 1
                else:
                    time_period_stats[region_id][prediction][flight_date]['night'] += 1

            if flight['duration_min']:
                duration_stats[region_id][prediction][flight_date].append(flight['duration_min'])
            
            # Обрабатываем eet_info - это строка, нужно извлечь числовое значение
            eet_str = flight.get('eet_info')
            if eet_str:
                try:
                    # Пытаемся извлечь число из строки (например, "120 мин" -> 120)
                    numbers = re.findall(r'\d+', str(eet_str))
                    if numbers:
                        eet_value = float(numbers[0])  # Берем первое найденное число
                        eet_stats[region_id][prediction][flight_date].append(eet_value)
                except (ValueError, TypeError):
                    # Если не удалось извлечь число, пропускаем
                    pass
            
            if flight.get('quantity'):
                quantity_stats[region_id][prediction][flight_date].append(flight['quantity'])
            
            # Обрабатываем altitude_info - это строка, нужно извлечь числовое значение
            altitude_str = flight.get('altitude')
            if altitude_str:
                try:
                    # Пытаемся извлечь число из строки (например, "1000 м" -> 1000)
                    numbers = re.findall(r'\d+', str(altitude_str))
                    if numbers:
                        altitude_value = float(numbers[0])  # Берем первое найденное число
                        altitude_stats[region_id][prediction][flight_date].append(altitude_value)
                except (ValueError, TypeError):
                    # Если не удалось извлечь число, пропускаем
                    pass

        return daily_stats, hourly_stats, time_period_stats, duration_stats, eet_stats, quantity_stats, altitude_stats

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

    def populate_region_stats(self, start_date: date, end_date: date, start_date_prediction: date, end_date_prediction: date):
        """Заполнение таблицы region_stats расчетными данными с новым алгоритмом zero_days"""
        cursor = None
        try:
            start_time = time.time()
            cursor = self.connection.cursor()

            # Получаем данные о полетах
            flights_data = self.get_flights_data(start_date, end_date)
            logging.info(f"Получено {len(flights_data)} записей о полетах для обработки")
            
            if not flights_data:
                logging.warning("Нет данных о полетах для обработки")
                return
                
            daily_stats, hourly_stats, time_period_stats, duration_stats, eet_stats, quantity_stats, altitude_stats = self.calculate_stats(
                flights_data, start_date, end_date
            )
            
            # Получаем ВСЕ регионы из таблицы regions (по ID)
            all_region_ids = self.get_all_regions()
            if not all_region_ids:
                logging.warning("Не найдено регионов для обработки")
                return
            
            logging.info(f"Всего регионов для обработки: {len(all_region_ids)}")
            
            # Получаем области и названия регионов
            self.get_region_areas_and_ids()
            
            # Логируем статистику по регионам с данными
            regions_with_data = set(daily_stats.keys())
            logging.info(f"Регионов с данными о полетах: {len(regions_with_data)}")
            
            for region_id, prediction_data in daily_stats.items():
                region_name = self.region_names.get(region_id, f"ID:{region_id}")
                for prediction_type, date_data in prediction_data.items():
                    total_flights = sum(date_data.values())
                    logging.info(f"Регион {region_name} (ID:{region_id}, {prediction_type}): {total_flights} полетов")
            
            batch_values = []

            # Словарь для отслеживания последовательных дней без полетов по регионам и типам полетов
            region_zero_days = defaultdict(lambda: defaultdict(int))

            # Обрабатываем каждый день в диапазоне
            current_date = start_date
            while current_date <= end_date:
                if current_date.day % 10 == 0:
                    logging.info(f"Обработка дата: {current_date}")

                for region_id in all_region_ids:
                    # Обрабатываем оба типа полетов: настоящие ('download') и прогнозные ('prediction')
                    for prediction_type in ['download', 'prediction']:
                        # Пропускаем обработку прогнозных данных вне диапазона start_date_prediction - end_date_prediction
                        if prediction_type == 'prediction' and current_date < start_date_prediction or current_date > end_date_prediction:
                            continue
                        # Пропускаем обработку настоящих данных после start_date_prediction
                        if prediction_type == 'download' and current_date >= start_date_prediction:
                            continue
                        # Получаем статистику для текущего дня, региона и типа полетов
                        daily_count = daily_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, 0)

                        # Вычисляем количество полетов по времени суток
                        morning = time_period_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, {}).get('morning', 0)
                        afternoon = time_period_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, {}).get('afternoon', 0)
                        evening = time_period_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, {}).get('evening', 0)
                        night = time_period_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, {}).get('night', 0)

                        # Общее количество полетов за день - используем daily_count как основной источник
                        # и проверяем соответствие с суммой по времени суток
                        total_flights = daily_count
                        time_periods_sum = morning + afternoon + evening + night
                        
                        # Если есть расхождение, используем большее значение и логируем
                        if total_flights != time_periods_sum:
                            # logging.warning(f"Расхождение в подсчете полетов для {region} {current_date} {prediction_type}: daily_count={total_flights}, time_periods_sum={time_periods_sum}")
                            total_flights = max(total_flights, time_periods_sum)

                        # Обновляем счетчик дней без полетов
                        if total_flights > 0:
                            region_zero_days[region_id][prediction_type] = 0  # Сбрасываем счетчик
                        else:
                            region_zero_days[region_id][prediction_type] += 1  # Увеличиваем счетчик

                        # Вычисляем среднюю длительность полетов
                        durations = duration_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, [])
                        avg_duration = int(statistics.mean(durations)) if durations else 0

                        # Вычисляем среднее расчетное время полета
                        eet_values = eet_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, [])
                        avg_eet = round(statistics.mean(eet_values), 2) if eet_values else 0

                        # Вычисляем среднее количество БПЛА
                        quantity_values = quantity_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, [])
                        avg_quantity = round(statistics.mean(quantity_values), 2) if quantity_values else 0

                        # Вычисляем среднюю высоту полета
                        altitude_values = altitude_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, [])
                        avg_altitude = round(statistics.mean(altitude_values), 2) if altitude_values else 0

                        # Пиковая нагрузка - максимальное количество полетов за час в этот день
                        hourly_data = hourly_stats.get(region_id, {}).get(prediction_type, {}).get(current_date, {})
                        peak_load = max(hourly_data.values()) if hourly_data else 0

                        # Плотность полетов
                        area = self.region_areas.get(region_id, 1)
                        flight_density = self.safe_calculate_flight_density(total_flights, area)

                        # Получаем название региона
                        region_name = self.region_names.get(region_id, None)

                        # Для остальных полей используем значения по умолчанию
                        # (эти поля будут обновляться в другом методе)
                        batch_values.append((
                            region_id,  # region_id - первичный ключ
                            region_name,  # region - для удобства
                            str(current_date),
                            prediction_type,  # prediction
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
                            region_zero_days[region_id][prediction_type],  # zero_days по новому алгоритму
                            avg_duration,
                            avg_eet,  # eet_info
                            avg_quantity,  # quantity
                            avg_altitude  # altitude_info
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
        """Вычисление медианного числа полетов в сутки по месяцам (по region_id)"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Получаем все daily_flights по месяцам, регионам и типам полетов
            cursor.execute("""
                SELECT region_id, prediction, DATE_FORMAT(date, '%Y-%m') as month, total_flights
                FROM region_stats
                ORDER BY region_id, prediction, month, total_flights
            """)

            data = cursor.fetchall()
            logging.info(f"Получено {len(data)} записей для вычисления медианы")

            # Группируем данные по region_id, типу полетов и месяцу
            grouped_data = defaultdict(list)
            for row in data:
                key = (row['region_id'], row['prediction'], row['month'])
                grouped_data[key].append(row['total_flights'])

            logging.info(f"Сгруппировано {len(grouped_data)} групп для вычисления медианы")

            # Вычисляем медиану для каждой группы
            median_results = {}
            for key, values in grouped_data.items():
                if values:
                    median_results[key] = statistics.median(values)
                else:
                    median_results[key] = 0

            logging.info(f"Вычислено {len(median_results)} медианных значений")
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

            # Проверяем, есть ли данные в region_stats
            cursor.execute("SELECT COUNT(*) as count FROM region_stats")
            region_stats_count = cursor.fetchone()['count']
            logging.info(f"Записей в region_stats: {region_stats_count}")
            
            if region_stats_count == 0:
                logging.warning("Таблица region_stats пуста, пропускаем заполнение region_stats_month")
                return
            
            # Получаем агрегированные данные по месяцам (без медианы), группируем по region_id
            logging.info("Выполняем агрегацию данных из region_stats...")
            cursor.execute("""
                SELECT 
                    region_id,
                    MAX(region) as region_name,
                    prediction,
                    DATE_FORMAT(date, '%Y-%m') as month,
                    SUM(total_flights) as total_flights,
                    AVG(CASE WHEN total_flights > 0 THEN avg_duration_min ELSE NULL END) as avg_flight_duration,
                    MAX(peak_load) as peak_load,
                    SUM(morning_flights) as morning_flights,
                    SUM(afternoon_flights) as afternoon_flights,
                    SUM(evening_flights) as evening_flights,
                    SUM(night_flights) as night_flights,
                    MAX(zero_days) as max_zero_days,
                    AVG(CASE WHEN total_flights > 0 THEN eet_info ELSE NULL END) as avg_eet_info,
                    AVG(CASE WHEN total_flights > 0 THEN quantity ELSE NULL END) as avg_quantity,
                    AVG(CASE WHEN total_flights > 0 THEN altitude_info ELSE NULL END) as avg_altitude_info
                FROM region_stats
                GROUP BY region_id, prediction, DATE_FORMAT(date, '%Y-%m')
                ORDER BY region_id, prediction, month
            """)
            monthly_data = cursor.fetchall()
            logging.info(f"Получено {len(monthly_data)} агрегированных записей для region_stats_month")
            
            if monthly_data:
                logging.info("Пример агрегированной записи:")
                logging.info(f"  {monthly_data[0]}")
            else:
                logging.warning("Нет агрегированных данных для region_stats_month")

            # Вычисляем медиану daily_flights
            logging.info("Вычисляем медиану daily_flights...")
            median_daily_flights = self.calculate_median_daily_flights()
            logging.info(f"Вычислено {len(median_daily_flights)} медианных значений")

            # Получаем площади регионов для расчета плотности
            self.get_region_areas_and_ids()

            # Вычисляем изменение по сравнению с предыдущим месяцем
            prev_month_data = defaultdict(dict)
            batch_values = []
            
            logging.info(f"Начинаем обработку {len(monthly_data)} агрегированных записей...")

            for i, row in enumerate(monthly_data):
                if i % 100 == 0:  # Логируем каждые 100 записей
                    logging.info(f"Обработано {i} из {len(monthly_data)} записей")
                region_id = row['region_id']
                region_name = row['region_name']
                month = row['month']
                prediction = row['prediction']

                # Рассчитываем плотность полетов
                area = self.region_areas.get(region_id, 1)
                flight_density = self.safe_calculate_flight_density(row['total_flights'], area)
                
                # flight_density теперь использует double, ограничения не нужны

                # Вычисляем изменение по сравнению с предыдущим месяцем
                monthly_change = 0.0
                if region_id in prev_month_data and prediction in prev_month_data[region_id]:
                    prev_total = prev_month_data[region_id][prediction]
                    if prev_total > 0:
                        # Преобразуем Decimal к float для вычислений
                        current_total_float = float(row['total_flights'])
                        prev_total_float = float(prev_total)
                        monthly_change = ((current_total_float - prev_total_float) / prev_total_float) * 100
                    elif row['total_flights'] > 0:
                        monthly_change = 100.0
                
                # monthly_change теперь использует double, ограничения не нужны

                # Сохраняем данные для следующего месяца
                prev_month_data[region_id][prediction] = row['total_flights']

                # Преобразуем среднюю длительность к float, если необходимо
                avg_duration = row['avg_flight_duration']
                if isinstance(avg_duration, Decimal):
                    avg_duration = float(avg_duration)
                
                # avg_flight_duration теперь использует double, ограничения не нужны

                # Преобразуем новые поля к float, если необходимо
                avg_eet = row['avg_eet_info']
                if isinstance(avg_eet, Decimal):
                    avg_eet = float(avg_eet)
                
                # eet_info теперь использует double, ограничения не нужны

                avg_quantity = row['avg_quantity']
                if isinstance(avg_quantity, Decimal):
                    avg_quantity = float(avg_quantity)
                
                # quantity теперь использует double, ограничения не нужны

                avg_altitude = row['avg_altitude_info']
                if isinstance(avg_altitude, Decimal):
                    avg_altitude = float(avg_altitude)
                
                # altitude_info теперь использует double, ограничения не нужны

                # Рассчитываем проценты полетов по времени суток
                total = float(row['total_flights'])
                morning_percent = (float(row['morning_flights']) / total * 100) if total > 0 else 0
                afternoon_percent = (float(row['afternoon_flights']) / total * 100) if total > 0 else 0
                evening_percent = (float(row['evening_flights']) / total * 100) if total > 0 else 0
                night_percent = (float(row['night_flights']) / total * 100) if total > 0 else 0
                
                # Проценты теперь используют double, ограничения не нужны

                # Получаем медиану daily_flights (ключ теперь по region_id)
                median_key = (region_id, prediction, month)
                median_daily = median_daily_flights.get(median_key, 0)
                
                # median_daily_flights теперь использует double, ограничения не нужны

                batch_values.append((
                    region_id,                 # region_id - первичный ключ
                    region_name,               # region - для удобства
                    month,                     # month
                    prediction,                # prediction
                    int(row['total_flights']), # total_flights
                    round(avg_duration or 0, 2), # avg_flight_duration
                    row['peak_load'],          # peak_load
                    round(flight_density, 6),  # flight_density
                    round(monthly_change, 2),  # monthly_change
                    row['morning_flights'],    # morning_flights
                    row['afternoon_flights'],  # afternoon_flights
                    row['evening_flights'],    # evening_flights
                    row['night_flights'],      # night_flights
                    round(morning_percent, 2), # morning_percent
                    round(afternoon_percent, 2), # afternoon_percent
                    round(evening_percent, 2), # evening_percent
                    round(night_percent, 2),   # night_percent
                    round(median_daily, 2),    # median_daily_flights
                    row['max_zero_days'],      # zero_days
                    round(avg_eet or 0, 2),    # eet_info
                    round(avg_quantity or 0, 2), # quantity
                    round(avg_altitude or 0, 2)  # altitude_info
                ))
            
            logging.info(f"Обработка завершена. Подготовлено {len(batch_values)} записей для вставки")

            # Выполняем вставку
            if batch_values:
                logging.info(f"Подготовлено {len(batch_values)} записей для вставки в region_stats_month")
                logging.info(f"Пример записи: {batch_values[0] if batch_values else 'Нет данных'}")
                self.execute_batch_insert(cursor, batch_values, 'region_stats_month')
                self.connection.commit()
                logging.info("Вставка в region_stats_month завершена успешно")
            else:
                logging.warning("Нет данных для вставки в region_stats_month")

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
                    (region_id, region, date, prediction, peak_load, avg_daily_flights, median_daily_flights, 
                     monthly_change, flight_density, morning_flights, afternoon_flights, 
                     evening_flights, night_flights, total_flights, zero_days, avg_duration_min,
                     eet_info, quantity, altitude_info)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, batch_values)
            elif table_name == 'region_stats_month':
                cursor.executemany("""
                    INSERT INTO region_stats_month 
                    (region_id, region, month, prediction, total_flights, avg_flight_duration, peak_load,
                     flight_density, monthly_change, morning_flights, afternoon_flights,
                     evening_flights, night_flights, morning_percent, afternoon_percent,
                     evening_percent, night_percent, median_daily_flights, zero_days,
                     eet_info, quantity, altitude_info)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

            # Получаем даты из настроек
            start_date_str = self.get_setting_value('start_date', '2024-01-01')
            end_date_str = self.get_setting_value('end_date', '2025-12-31')

            start_date_prediction_str = self.get_setting_value('start_date_prediction', '2025-08-01')
            end_date_prediction_str = self.get_setting_value('end_date_prediction', '2025-12-31')

            # Преобразуем строки в объекты date
            try:
                start_date = date.fromisoformat(start_date_str)
                end_date = date.fromisoformat(end_date_str)
                start_date_prediction = date.fromisoformat(start_date_prediction_str)
                end_date_prediction = date.fromisoformat(end_date_prediction_str)
                logging.info(f"Используются даты из настроек: {start_date} - {end_date}")
            except ValueError as e:
                logging.warning(f"Ошибка парсинга дат из настроек: {e}. Используются значения по умолчанию")
    

            # Заполняем данными
            self.populate_region_stats(start_date, end_date, start_date_prediction, end_date_prediction) #, prediction='download'
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
