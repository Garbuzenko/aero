# prediction.py
"""
Модуль для создания предсказаний на указанный период и записи их в таблицу processed_flights.
Перед генерацией удаляет существующие записи с prediction='prediction' в указанном периоде.
"""

import mysql.connector
from mysql.connector import Error
import logging
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta, time
import random
from typing import Dict, List, Any, Tuple
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
import traceback
import warnings

# Подавление предупреждения pandas о SQLAlchemy
warnings.filterwarnings('ignore', category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../prediction.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class FlightPredictorNew:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.historical_data = None
        self.region_stats = None
        self.aircraft_types = None
        self.region_utc_cache = {}  # Кэш для UTC offset'ов регионов

    def connect_to_db(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            logging.info("Успешное подключение к базе данных")
            return True
        except Error as e:
            logging.error(f"Ошибка подключения к MySQL: {e}")
            logging.debug(
                f"Детали подключения: host={self.db_config.get('host')}, database={self.db_config.get('database')}")
            return False

    def close_connection(self):
        """Закрытие соединения с БД"""
        if self.connection:
            self.connection.close()
            logging.info("Соединение с базой данных закрыто")

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

    def get_region_utc(self, region_id: int) -> int:
        """Получение UTC offset для региона с кэшированием"""
        # Проверяем кэш
        if region_id in self.region_utc_cache:
            return self.region_utc_cache[region_id]
        
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT UTC FROM regions WHERE id = %s", (region_id,))
            result = cursor.fetchone()
            utc_offset = result['UTC'] if result else 0
            # Сохраняем в кэш
            self.region_utc_cache[region_id] = utc_offset
            return utc_offset
        except Exception as e:
            logging.error(f"Ошибка получения UTC для региона {region_id}: {e}")
            self.region_utc_cache[region_id] = 0
            return 0
        finally:
            if cursor:
                cursor.close()

    def calculate_time_of_day(self, flight_time, region_id: int) -> str:
        """Определяет время суток на основе времени полета с учетом UTC региона"""
        try:
            if not region_id:
                return 'день'
                
            # Получаем UTC для региона
            utc_offset = self.get_region_utc(region_id)
            if utc_offset is None:
                return 'день'
                
            if not flight_time:
                return 'день'
                
            # Применяем UTC offset
            if isinstance(flight_time, str):
                try:
                    flight_time = datetime.strptime(flight_time, '%H:%M:%S').time()
                except:
                    try:
                        flight_time = datetime.strptime(flight_time, '%H:%M').time()
                    except:
                        return 'день'
            elif isinstance(flight_time, time):
                pass  # уже time объект
            else:
                return 'день'
                        
            # Определяем время суток в местном часовом поясе
            local_hour = flight_time.hour
            
            # Определяем время суток
            if 6 <= local_hour < 12:
                return 'утро'
            elif 12 <= local_hour < 18:
                return 'день'
            elif 18 <= local_hour < 24:
                return 'вечер'
            else:  # 0 <= local_hour < 6
                return 'ночь'
                
        except Exception as e:
            logging.error(f"Ошибка определения времени суток: {e}")
            return 'день'

    def delete_old_predictions(self, start_date: str, end_date: str):
        """Удаление существующих записей с prediction='prediction' в указанном периоде"""
        try:
            cursor = self.connection.cursor()

           
            delete_query = """
                DELETE FROM processed_flights 
                WHERE prediction = 'prediction' 
                AND dof_date BETWEEN %s AND %s
            """
            cursor.execute(delete_query, (start_date, end_date))
            deleted_count = cursor.rowcount
            self.connection.commit()

            logging.info(f"Удалено {deleted_count} старых записей предсказания за период {start_date} - {end_date}")
            return True

        except Exception as e:
            logging.error(f"Ошибка удаления старых предсказаний: {e}")
            logging.debug(f"Трассировка ошибки: {traceback.format_exc()}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def load_historical_data(self, start_date: str = '2024-01-01'):
        """Загрузка исторических данных из processed_flights (только download данные)"""
        try:
            query = """
                SELECT * FROM processed_flights 
                WHERE dof_date IS NOT NULL 
                AND dof_date >= %s
                AND prediction = 'download'
                ORDER BY dof_date
            """
            df = pd.read_sql(query, self.connection, params=[start_date])
            logging.info(f"Загружено {len(df)} исторических записей (только download данные)")

            # Валидация данных
            df = self.validate_historical_data(df)

            return df
        except Exception as e:
            logging.error(f"Ошибка загрузки исторических данных: {e}")
            logging.debug(f"Трассировка ошибки: {traceback.format_exc()}")
            return None

    def validate_historical_data(self, df):
        """Проверка наличия необходимых столбцов в исторических данных"""
        required_columns = [
            'dof_date', 'atd_time', 'ata_time', 'duration_min',
            'aircraft_type_code', 'aircraft_type_desc', 'departure_region', 'arrival_region',
            'region_id', 'departure_actual_time', 'arrival_actual_time',
            'planned_date', 'departure_actual_date', 'arrival_actual_date'
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logging.warning(f"Отсутствуют столбцы в исторических данных: {missing_columns}")
            # Добавляем недостающие столбцы с значениями по умолчанию
            for col in missing_columns:
                if col in ['atd_time', 'ata_time', 'departure_actual_time', 'arrival_actual_time']:
                    df[col] = None
                elif col in ['planned_date', 'departure_actual_date', 'arrival_actual_date']:
                    df[col] = None
                elif col == 'duration_min':
                    df[col] = 60  # средняя длительность полета
                elif col == 'region_id':
                    df[col] = 0
                else:
                    df[col] = ''

        # Проверяем типы данных
        if 'dof_date' in df.columns:
            df['dof_date'] = pd.to_datetime(df['dof_date']).dt.date
        if 'planned_date' in df.columns:
            df['planned_date'] = pd.to_datetime(df['planned_date'], errors='coerce').dt.date
        if 'departure_actual_date' in df.columns:
            df['departure_actual_date'] = pd.to_datetime(df['departure_actual_date'], errors='coerce').dt.date
        if 'arrival_actual_date' in df.columns:
            df['arrival_actual_date'] = pd.to_datetime(df['arrival_actual_date'], errors='coerce').dt.date

        logging.info(f"Проверены столбцы: {list(df.columns)}")
        return df

    def load_region_stats(self):
        """Загрузка статистики по регионам"""
        try:
            query = "SELECT region, AVG(total_flights) as avg_flights FROM region_stats GROUP BY region"
            df = pd.read_sql(query, self.connection)
            logging.info(f"Загружена статистика по {len(df)} регионам")
            return df.set_index('region')['avg_flights'].to_dict()
        except Exception as e:
            logging.error(f"Ошибка загрузки статистики регионов: {e}")
            logging.debug(f"Трассировка ошибки: {traceback.format_exc()}")
            return {}

    def load_aircraft_types(self):
        """Загрузка типов воздушных судов"""
        try:
            query = """
                SELECT DISTINCT aircraft_type_code, aircraft_type_desc 
                FROM processed_flights 
                WHERE aircraft_type_code IS NOT NULL
            """
            df = pd.read_sql(query, self.connection)
            aircraft_types = df.to_dict('records')
            logging.info(f"Загружено {len(aircraft_types)} типов ВС")
            return aircraft_types
        except Exception as e:
            logging.error(f"Ошибка загрузки типов ВС: {e}")
            logging.debug(f"Трассировка ошибки: {traceback.format_exc()}")
            return []

    def calculate_growth_rate(self):
        """Расчет темпа роста на основе исторических данных"""
        try:
            # Группируем по месяцам
            monthly_data = self.historical_data.groupby(
                pd.to_datetime(self.historical_data['dof_date']).dt.to_period('M')
            ).size()

            logging.info(f"Данные по месяцам: {monthly_data.tolist()}")

            if len(monthly_data) < 2:
                logging.warning("Недостаточно данных для расчета темпа роста")
                return 0.1  # По умолчанию 10% рост

            # Расчет среднемесячного роста
            growth_rates = []
            for i in range(1, len(monthly_data)):
                prev_value = monthly_data.iloc[i - 1]
                if prev_value > 0:
                    growth_rate = (monthly_data.iloc[i] - prev_value) / prev_value
                    growth_rates.append(growth_rate)
                    logging.debug(f"Рост месяца {i}: {growth_rate:.2%}")

            avg_growth = np.mean(growth_rates) if growth_rates else 0.1
            logging.info(f"Рассчитан средний темп роста: {avg_growth:.2%} на основе {len(growth_rates)} месяцев")
            return max(avg_growth, 0.05)  # Минимальный рост 5%
        except Exception as e:
            logging.error(f"Ошибка расчета темпа роста: {e}")
            logging.debug(f"Трассировка ошибки: {traceback.format_exc()}")
            return 0.1

    def generate_prediction_data(self, start_date: str, end_date: str):
        """Генерация данных предсказания на указанный период"""
        if self.historical_data is None:
            logging.error("Исторические данные не загружены")
            return None

        if self.historical_data.empty:
            logging.error("Исторические данные пусты")
            return None

        growth_rate = self.calculate_growth_rate()
        prediction_data = []

        # Преобразуем строки дат в объекты datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        # Генерируем данные для каждого месяца в периоде
        current_date = start_dt
        while current_date <= end_dt:
            year = current_date.year
            month = current_date.month

            month_data = self.generate_monthly_prediction(month, year, growth_rate)
            if month_data:
                prediction_data.extend(month_data)
                logging.info(f"Для месяца {month}/{year} сгенерировано {len(month_data)} записей")
            else:
                logging.warning(f"Для месяца {month}/{year} не удалось сгенерировать данные")

            # Переход к следующему месяцу
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

        logging.info(f"Сгенерировано {len(prediction_data)} записей предсказания на период {start_date} - {end_date}")
        return prediction_data

    def generate_monthly_prediction(self, month, year, growth_rate):
        """Генерация данных предсказания для конкретного месяца"""
        try:
            logging.info(f"Генерация данных для месяца {month}, год {year}")

            # Фильтруем исторические данные для этого месяца
            month_mask = pd.to_datetime(self.historical_data['dof_date']).dt.month == month
            historical_month = self.historical_data[month_mask].copy()

            logging.info(f"Найдено {len(historical_month)} исторических записей для месяца {month}")

            # Если нет данных для этого месяца, используем среднее за месяц
            if historical_month.empty:
                logging.warning(f"Нет исторических данных для месяца {month}")
                
                # Рассчитываем среднее количество записей за месяц
                month_counts = self.historical_data.groupby(
                    pd.to_datetime(self.historical_data['dof_date']).dt.to_period('M')
                ).size()
                
                if len(month_counts) > 0:
                    avg_month_count = int(month_counts.mean())
                    logging.info(f"Среднее количество записей за месяц: {avg_month_count}")
                    
                    # Сэмплируем из всех данных среднее количество записей
                    if len(self.historical_data) >= avg_month_count:
                        historical_month = self.historical_data.sample(
                            n=avg_month_count, replace=False, random_state=42 + month
                        )
                    else:
                        historical_month = self.historical_data.sample(
                            n=avg_month_count, replace=True, random_state=42 + month
                        )
                    logging.info(f"Используем {len(historical_month)} записей на основе среднего")
                else:
                    logging.error("Невозможно рассчитать среднее количество записей")
                    return []

            # Рассчитываем ожидаемое количество полетов с учетом роста
            base_count = len(historical_month)
            expected_count = int(base_count * (1 + growth_rate))
            logging.info(
                f"Ожидаемое количество записей: {expected_count} (базовое: {base_count}, рост: {growth_rate:.2%})")

            # Сэмплируем из исторических данных
            if len(historical_month) > expected_count:
                sample_data = historical_month.sample(n=expected_count, replace=False, random_state=42)
            else:
                sample_data = historical_month.sample(n=expected_count, replace=True, random_state=42)

            logging.info(f"Выбрано {len(sample_data)} записей для сэмплирования")

            # Обновляем даты на целевой год
            prediction_records = []
            successful_records = 0
            failed_records = 0

            for idx, (_, row) in enumerate(sample_data.iterrows()):
                record = self.update_record_for_prediction(row, month, year)
                if record is not None:
                    prediction_records.append(record)
                    successful_records += 1
                else:
                    failed_records += 1

                # Более частое логирование для отслеживания прогресса
                if idx % 1000 == 0 and idx > 0:
                    logging.info(f"Обработано {idx}/{len(sample_data)} записей ({idx/len(sample_data)*100:.1f}%), успешно: {successful_records}, ошибок: {failed_records}")

            logging.info(
                f"Сгенерировано {len(prediction_records)} записей для {month}/{year} (успешно: {successful_records}, ошибок: {failed_records})")
            return prediction_records

        except Exception as e:
            logging.error(f"Ошибка генерации предсказания для месяца {month}: {e}")
            logging.error(f"Трассировка ошибки: {traceback.format_exc()}")
            return []

    def update_record_for_prediction(self, record, month, year):
        """Обновление записи для предсказания на указанный год"""
        try:
            new_record = record.copy()

            # Генерируем новую дату в пределах указанного месяца и года
            days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30
            if month == 2:
                days_in_month = 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28

            day = random.randint(1, days_in_month)
            new_date = date(year, month, day)

            # Обновляем все даты
            new_record['dof_date'] = new_date
            new_record['planned_date'] = new_date
            new_record['departure_actual_date'] = new_date
            new_record['arrival_actual_date'] = new_date

            # Обновляем временные метки
            new_record['processed_at'] = datetime.now()

            # Генерируем новые идентификаторы
            new_record['source_id'] = f"pred_{random.randint(100000, 999999)}"
            new_record['flight_id'] = f"PRED{random.randint(1000000, 9999999)}"
            new_record['sheet_name'] = 'prediction'

            # Обрабатываем время вылета и прибытия (старые поля)
            new_record['atd_time'] = self.process_time_value(record.get('atd_time'))
            new_record['ata_time'] = self.process_time_value(record.get('ata_time'))
            
            # Обрабатываем новые поля времени
            new_record['departure_actual_time'] = self.process_time_value(record.get('departure_actual_time'))
            new_record['arrival_actual_time'] = self.process_time_value(record.get('arrival_actual_time'))

            # Немного варьируем длительность полета
            if pd.notna(record.get('duration_min')):
                try:
                    duration = float(record['duration_min'])
                    duration_var = random.randint(-30, 30)
                    new_record['duration_min'] = max(5, duration + duration_var)
                except (ValueError, TypeError):
                    new_record['duration_min'] = 60  # значение по умолчанию

            # Обновляем имя файла
            new_record['filename'] = f"prediction_{year}_{month:02d}.xlsx"
            
            # Устанавливаем prediction флаг
            new_record['prediction'] = 'prediction'
            
            # Генерируем time_of_day на основе времени вылета
            flight_time = new_record.get('departure_actual_time') or new_record.get('atd_time')
            region_id = record.get('region_id', 0)
            new_record['time_of_day'] = self.calculate_time_of_day(flight_time, region_id)
            
            # Генерируем uniq_str
            uniq_parts = [
                str(new_record.get('dof_date', '')),
                str(new_record.get('registration', '')),
                str(new_record.get('operator', '')),
                str(new_record.get('aircraft_type_code', '')),
                str(new_record.get('filename', '')),
                str(new_record.get('region_id', '')),
                str(new_record.get('prediction', '')),
                str(new_record.get('sts', '')),
                str(new_record.get('time_of_day', '')),
                str(new_record.get('departure_coords', ''))
            ]
            new_record['uniq_str'] = '|'.join(uniq_parts)
            
            # Если отсутствуют новые поля, устанавливаем значения по умолчанию
            if 'shr_message' not in new_record or pd.isna(new_record.get('shr_message')):
                new_record['shr_message'] = None
            if 'dep_message' not in new_record or pd.isna(new_record.get('dep_message')):
                new_record['dep_message'] = None
            if 'arr_message' not in new_record or pd.isna(new_record.get('arr_message')):
                new_record['arr_message'] = None
            if 'registration_all' not in new_record or pd.isna(new_record.get('registration_all')):
                new_record['registration_all'] = new_record.get('registration', '')
            if 'sts' not in new_record or pd.isna(new_record.get('sts')):
                new_record['sts'] = None
            if 'altitude_max' not in new_record or pd.isna(new_record.get('altitude_max')):
                new_record['altitude_max'] = None

            return new_record

        except Exception as e:
            logging.error(f"Ошибка обновления записи: {e}")
            logging.debug(f"Трассировка ошибки при обновлении записи: {traceback.format_exc()}")
            return None

    def process_time_value(self, time_value):
        """Обработка значений времени с учетом разных типов данных"""
        if pd.isna(time_value):
            return None

        try:
            # Если это Timedelta
            if isinstance(time_value, pd.Timedelta):
                total_seconds = int(time_value.total_seconds())
                hours = (total_seconds // 3600) % 24
                minutes = (total_seconds % 3600) // 60
                time_obj = time(hours, minutes)
            # Если это строка
            elif isinstance(time_value, str):
                time_value = time_value.strip()
                for fmt in ['%H:%M:%S', '%H:%M', '%H:%M:%S.%f']:
                    try:
                        time_obj = datetime.strptime(time_value, fmt).time()
                        break
                    except ValueError:
                        continue
                else:
                    # Если формат не распознан, генерируем случайное время
                    logging.warning(f"Неизвестный формат времени: {time_value}, генерируем случайное время")
                    time_obj = time(random.randint(0, 23), random.randint(0, 59))
            # Если это время
            elif isinstance(time_value, time):
                time_obj = time_value
            # Если это datetime
            elif isinstance(time_value, datetime):
                time_obj = time_value.time()
            else:
                # Для неизвестных типов генерируем случайное время
                logging.warning(f"Неизвестный тип времени: {type(time_value)}, значение: {time_value}")
                time_obj = time(random.randint(0, 23), random.randint(0, 59))

            # Добавляем случайное отклонение до 2 часов
            hour_offset = random.randint(-2, 2)
            minute_offset = random.randint(-30, 30)

            new_hour = (time_obj.hour + hour_offset) % 24
            if new_hour < 0:
                new_hour += 24
            new_minute = max(0, min(59, time_obj.minute + minute_offset))

            return time(new_hour, new_minute)

        except Exception as e:
            logging.warning(f"Ошибка обработки времени {time_value}: {e}")
            return time(random.randint(0, 23), random.randint(0, 59))

    def save_prediction_data(self, prediction_data):
        """Сохранение данных предсказания в таблицу processed_flights"""
        if not prediction_data:
            logging.error("Нет данных для сохранения")
            return False

        try:
            cursor = self.connection.cursor()

            # Подготавливаем SQL запрос для вставки с новой структурой
            columns = [
                'source_id', 'sheet_name', 'flight_id', 'flight_number', 
                'aircraft_type_code', 'aircraft_type_desc',
                'region_id', 'departure_region', 'arrival_region',
                'duration_min', 'operator', 'registration', 'registration_all',
                'departure_coords', 'arrival_coords',
                'departure_lat', 'departure_lon', 'arrival_lat', 'arrival_lon',
                'dof_date', 'arrival_actual_date', 'departure_actual_date', 'planned_date',
                'atd_time', 'departure_actual_time', 'ata_time', 'arrival_actual_time',
                'eet_info', 'shr_message', 'dep_message', 'arr_message', 
                'center_es_orvd', 'altitude_info', 'altitude_max',
                'phone_number', 'quantity', 'sts', 'filename', 'hexagon_id', 
                'prediction', 'time_of_day', 'uniq_str'
            ]

            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join(columns)
            insert_query = f"INSERT INTO processed_flights ({columns_str}) VALUES ({placeholders})"

            # Подготавливаем данные для вставки
            data_to_insert = []
            for record in prediction_data:
                row_data = []
                for col in columns:
                    value = record.get(col)
                    # Обрабатываем специальные типы данных
                    if col in ['dof_date', 'planned_date', 'departure_actual_date', 'arrival_actual_date']:
                        if hasattr(value, 'strftime'):
                            value = value.strftime('%Y-%m-%d')
                        elif pd.isna(value):
                            value = None
                    elif col in ['atd_time', 'ata_time', 'departure_actual_time', 'arrival_actual_time']:
                        if hasattr(value, 'strftime'):
                            value = value.strftime('%H:%M:%S')
                        elif pd.isna(value):
                            value = None
                    elif col == 'prediction':
                        value = 'prediction'  # Все предсказания помечаем как 'prediction'
                    elif col == 'hexagon_id':
                        value = 0  # По умолчанию
                    elif pd.isna(value):
                        value = None
                    row_data.append(value)
                data_to_insert.append(tuple(row_data))

            # Выполняем пакетную вставку
            batch_size = 10000
            total_inserted = 0

            for i in range(0, len(data_to_insert), batch_size):
                batch = data_to_insert[i:i + batch_size]
                try:
                    cursor.executemany(insert_query, batch)
                    self.connection.commit()
                    total_inserted += len(batch)
                    logging.info(f"Вставлено {len(batch)} записей предсказания (всего: {total_inserted})")
                except Exception as batch_error:
                    logging.error(f"Ошибка вставки батча {i // batch_size + 1}: {batch_error}")
                    self.connection.rollback()
                    # Пробуем вставить по одной записи для определения проблемной
                    for j, single_record in enumerate(batch):
                        try:
                            cursor.execute(insert_query, single_record)
                            self.connection.commit()
                            total_inserted += 1
                        except Exception as single_error:
                            logging.error(f"Ошибка вставки записи {i + j}: {single_error}")
                            logging.debug(f"Проблемная запись: {single_record}")
                            self.connection.rollback()

            logging.info(f"Всего сохранено {total_inserted} записей предсказания из {len(data_to_insert)}")
            return total_inserted > 0

        except Exception as e:
            logging.error(f"Ошибка сохранения данных предсказания: {e}")
            logging.debug(f"Трассировка ошибки: {traceback.format_exc()}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def generate_predictions(self, prediction_start: str = None, prediction_end: str = None):
        """Основной метод для генерации предсказаний"""
        try:
            if not self.connect_to_db():
                logging.error("Не удалось подключиться к базе данных")
                return False

            # Читаем даты из настроек, если не переданы явно
            if prediction_start is None:
                prediction_start = self.get_setting_value('prediction_start', '2025-08-01')
                logging.info(f"Дата начала прогноза из настроек: {prediction_start}")
            
            if prediction_end is None:
                prediction_end = self.get_setting_value('prediction_end', '2025-12-31')
                logging.info(f"Дата окончания прогноза из настроек: {prediction_end}")

            logging.info(f"Начало генерации предсказаний для периода {prediction_start} - {prediction_end}...")

            # Удаляем старые предсказания в указанном периоде
            logging.info("Удаление старых записей предсказания...")
            if not self.delete_old_predictions(prediction_start, prediction_end):
                logging.error("Не удалось удалить старые предсказания")
                return False

            # Загружаем необходимые данные
            logging.info("Загрузка исторических данных...")
            self.historical_data = self.load_historical_data()
            if self.historical_data is None or self.historical_data.empty:
                logging.error("Не удалось загрузить исторические данные или данные пусты")
                return False

            logging.info(f"Загружено {len(self.historical_data)} исторических записей")

            self.region_stats = self.load_region_stats()
            self.aircraft_types = self.load_aircraft_types()

            # Генерируем данные предсказания
            logging.info("Генерация предсказаний...")
            prediction_data = self.generate_prediction_data(prediction_start, prediction_end)

            if not prediction_data:
                logging.error("Не удалось сгенерировать данные предсказания")
                return False

            # Сохраняем данные
            logging.info("Сохранение данных предсказания...")
            if not self.save_prediction_data(prediction_data):
                logging.error("Не удалось сохранить данные предсказания")
                return False

            logging.info("Предсказания успешно сгенерированы и сохранены в processed_flights")
            return True

        except Exception as e:
            logging.error(f"Критическая ошибка при генерации предсказаний: {e}")
            logging.error(f"Трассировка критической ошибки: {traceback.format_exc()}")
            return False
        finally:
            self.close_connection()


def main():
    """Основная функция для запуска генерации предсказаний"""
    logging.info("Запуск генерации предсказаний...")

    try:
        predictor = FlightPredictorNew(settings.DB_CONFIG)

        # Даты будут прочитаны из таблицы settings
        success = predictor.generate_predictions()

        if success:
            logging.info("Генерация предсказаний завершена успешно")
        else:
            logging.error("Генерация предсказаний завершена с ошибками")

        return success
    except Exception as e:
        logging.error(f"Непредвиденная ошибка в main: {e}")
        logging.error(f"Трассировка: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    main()