# parser_file.py
"""
Модуль импорта и парсинга данных.
Загружает файлы с FTP, парсит данные и заполняет таблицу processed_flights.
"""
import mysql.connector
from mysql.connector import Error
import re
import logging
from datetime import datetime, date, time
import time as time_module
from typing import Optional, Dict, Any
import json
import ast
from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree
from shapely.prepared import prep
import pandas as pd
from ftplib import FTP
import os
# from utils import settings
from openpyxl import load_workbook

import settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../log.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class FlightDataProcessor:
    def __init__(self):
        self.connection = None
        self.regions = []
        self.region_tree = None
        self.sheet_structures = {}
        self.batch_data = []
        self.local_path = ""
        self.current_filename = None
        self.current_file_progress = 0
        self.total_records_in_file = 0

    def process_unprocessed_files(self):
        """Обрабатывает только те файлы, которые ещё не помечены как 'processed'."""
        if not self.connection or not self.connection.is_connected():
            if not self.connect_to_db():
                logging.error("Не удалось подключиться к БД для обработки файлов")
                return

        # Загрузка геоданных (если ещё не загружены)
        if not self.regions:
            if not self.load_regions_from_db():
                logging.error("Не удалось загрузить регионы. Прерывание обработки.")
                return

        # Получаем список файлов с FTP
        ftp_files = self.list_ftp_files()
        for ftp_file in ftp_files:
            try:
                if self.is_file_processed(ftp_file):
                    continue

                self.mark_file_processed(ftp_file, "process")
                self.current_filename = ftp_file
                self.current_file_progress = 0

                local_path = f"downloads/{ftp_file}"
                os.makedirs("downloads", exist_ok=True)

                if not self.download_ftp_file(f"{settings.FTP_CONFIG['remote_dir']}{ftp_file}", local_path):
                    self.mark_file_processed(ftp_file, "error", "Ошибка загрузки файла")
                    continue

                data = self.load_data_from_excel(local_path)
                if data is None:
                    self.mark_file_processed(ftp_file, "error", "Ошибка загрузки данных")
                    continue

                self.process_flights(data, limit=None, batch_size=10000)
                self.mark_file_processed(ftp_file, "processed")
                self.update_progress(1, 1, f"Файл обработан")

            except Exception as e:
                error_msg = f"Ошибка обработки файла {ftp_file}: {e}"
                logging.error(error_msg)
                self.mark_file_processed(ftp_file, "error", error_msg)

    def connect_to_db(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = mysql.connector.connect(**settings.DB_CONFIG)
            logging.info("Успешное подключение к базе данных")
            return True
        except Error as e:
            logging.error(f"Ошибка подключения к MySQL: {e}")
            return False

    def create_log_table(self):
        """Создание таблицы LOG для записи сообщений"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    message TEXT,
                    procent DECIMAL(5,2)
                )
            """)
            self.connection.commit()
            logging.info("Таблица log создана или уже существует")
        except Exception as e:
            logging.error(f"Ошибка создания таблицы log: {e}")
        finally:
            if cursor:
                cursor.close()

    def write_log(self, message, procent=None):
        """Запись сообщения в таблицу LOG"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO log (message, procent) VALUES (%s, %s)",
                           (message, procent))
            self.connection.commit()
        except Exception as e:
            logging.error(f"Ошибка записи в лог: {e}")
        finally:
            if cursor:
                cursor.close()

    def update_progress(self, current, total, stage="processing"):
        """Обновление прогресса выполнения"""
        if total == 0:
            return

        progress_percent = round((current / total) * 100, 2)
        self.current_file_progress = progress_percent

        # Записываем в лог
        log_message = f"{stage}: ({progress_percent}%)"
        self.write_log(log_message, progress_percent)

        # Обновляем поле procent в processed_files
        if self.current_filename:
            try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE processed_files 
                    SET procent = %s 
                    WHERE filename = %s
                """, (progress_percent, self.current_filename))
                self.connection.commit()
            except Exception as e:
                logging.error(f"Ошибка обновления прогресса: {e}")
            finally:
                if cursor:
                    cursor.close()

    def list_ftp_files(self):
        """Получение списка файлов с FTP"""
        try:
            ftp = FTP(settings.FTP_CONFIG['host'])
            ftp.login(settings.FTP_CONFIG['username'], settings.FTP_CONFIG['password'])
            ftp.cwd(settings.FTP_CONFIG['remote_dir'])
            files = ftp.nlst()
            ftp.quit()
            xlsx_files = [f for f in files if f.endswith('.xlsx')]
            logging.info(f"Найдено не обработанных файлов: {len(xlsx_files)}")
            self.update_progress(0, 1, f"Найдено не обработанных файлов: {len(xlsx_files)}")
            return xlsx_files
        except Exception as e:
            logging.error(f"Ошибка получения списка файлов с FTP: {e}")
            return []

    def download_ftp_file(self, remote_path, local_path):
        """Загрузка файла с FTP"""
        try:
            ftp = FTP(settings.FTP_CONFIG['host'])
            ftp.login(settings.FTP_CONFIG['username'], settings.FTP_CONFIG['password'])

            with open(local_path, 'wb') as f:
                ftp.retrbinary(f"RETR {remote_path}", f.write)

            ftp.quit()
            logging.info(f"Файл успешно загружен для обработки: {remote_path} -> {local_path}")
            self.update_progress(0, 1, f"Файл успешно загружен для обработки: {local_path}")
            return True
        except Exception as e:
            logging.error(f"Ошибка загрузки файла с FTP {remote_path}: {e}")
            return False

    def create_processed_files_table(self):
        """Создание таблицы для отслеживания обработанных файлов"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processed_files (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status ENUM('processed', 'error') NOT NULL,
                    error_message TEXT,
                    procent DECIMAL(5,2) DEFAULT 0.00,
                    UNIQUE KEY unique_filename (filename)
                ) COMMENT='Таблица для учета обработанных файлов'
            """)
            self.connection.commit()
            logging.info("Таблица processed_files создана или уже существует")
        except Exception as e:
            logging.error(f"Ошибка создания таблица processed_files: {e}")
        finally:
            if cursor:
                cursor.close()

    def mark_file_processed(self, filename, status="processed", error_message=None):
        """Отметка файла как обработанного"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO processed_files (filename, status, error_message, procent)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                status = VALUES(status),
                error_message = VALUES(error_message),
                processed_at = CURRENT_TIMESTAMP,
                procent = VALUES(procent)
            """, (filename, status, error_message, self.current_file_progress))
            self.connection.commit()
        except Exception as e:
            logging.error(f"Ошибка отметки файла как обработанного: {e}")
        finally:
            if cursor:
                cursor.close()

    def is_file_processed(self, filename):
        """Проверка, был ли файл уже обработан"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT status FROM processed_files WHERE filename = %s", (filename,))
            result = cursor.fetchone()
            return result is not None and result[0] == "processed"
        except Exception as e:
            logging.error(f"Ошибка проверки статуса файла: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def detect_sheet_structure(self, sheet_name, df):
        """Определение структуры листа Excel"""
        structure = {
            'has_shr': False,
            'has_dep': False,
            'has_arr': False,
            'date_column': None,
            'shr_column': None,
            'dep_column': None,
            'arr_column': None,
            'center_column': None
        }

        for col in df.columns:
            col_lower = str(col).lower()
            if 'shr' in col_lower:
                structure['has_shr'] = True
                structure['shr_column'] = col
            elif 'dep' in col_lower and 'arr' not in col_lower:
                structure['has_dep'] = True
                structure['dep_column'] = col
            elif 'arr' in col_lower:
                structure['has_arr'] = True
                structure['arr_column'] = col
            elif 'центр' in col_lower or 'center' in col_lower:
                structure['center_column'] = col
            elif 'дата' in col_lower or 'date' in col_lower:
                structure['date_column'] = col

        logging.info(f"Структура листа '{sheet_name}': {structure}")

        return structure

    def load_data_from_excel(self, file_path):
        """Загрузка данных из Excel файла с поддержкой нескольких листов"""
        try:
            # Загружаем книгу Excel
            wb = load_workbook(file_path)
            all_data = []
            f = 0
            for sheet_name in wb.sheetnames:
                df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                f = f + 1
                if df.empty:
                    continue

                # Определяем структуру листа
                structure = self.detect_sheet_structure(sheet_name, df)
                self.update_progress(f, len(wb.sheetnames)*10, f"Обработка листа '{sheet_name}'")
                self.sheet_structures[sheet_name] = structure

                # Добавляем информацию о листе в каждую запись
                for idx, row in df.iterrows():
                    row_dict = row.to_dict()
                    row_dict['sheet_name'] = sheet_name
                    row_dict['sheet_structure'] = structure
                    row_dict['source_id'] = idx  # Используем индекс как временный ID
                    all_data.append(row_dict)

            logging.info(f"Загружено {len(all_data)} записей из {len(wb.sheetnames)} листов Excel файла")
            return all_data

        except Exception as e:
            error_msg = f"Ошибка загрузки данных из Excel {file_path}: {e}"
            logging.error(error_msg)
            return None

    def extract_messages(self, row):
        """Извлечение текстов SHR, DEP, ARR из строки"""
        structure = row.get('sheet_structure', {})

        messages = {
            'shr': None,
            'dep': None,
            'arr': None
        }

        # Извлекаем SHR
        if structure.get('has_shr') and structure.get('shr_column'):
            shr_value = row.get(structure['shr_column'])
            # Преобразуем float в строку, если нужно
            if isinstance(shr_value, float) and not pd.isna(shr_value):
                shr_value = str(int(shr_value)) if shr_value.is_integer() else str(shr_value)
            if shr_value and not pd.isna(shr_value):
                messages['shr'] = str(shr_value)

        # Если нет отдельной колонки SHR, ищем в других колонках
        if not messages['shr']:
            for col, value in row.items():
                if isinstance(value, str) and value.startswith('(SHR-'):
                    messages['shr'] = value
                    break

        # Извлекаем DEP
        if structure.get('has_dep') and structure.get('dep_column'):
            dep_value = row.get(structure['dep_column'])
            # Преобразуем float в строку, если нужно
            if isinstance(dep_value, float) and not pd.isna(dep_value):
                dep_value = str(int(dep_value)) if dep_value.is_integer() else str(dep_value)
            if dep_value and not pd.isna(dep_value):
                messages['dep'] = str(dep_value)

        # Извлекаем ARR
        if structure.get('has_arr') and structure.get('arr_column'):
            arr_value = row.get(structure['arr_column'])
            # Преобразуем float в строку, если нужно
            if isinstance(arr_value, float) and not pd.isna(arr_value):
                arr_value = str(int(arr_value)) if arr_value.is_integer() else str(arr_value)
            if arr_value and not pd.isna(arr_value):
                messages['arr'] = str(arr_value)

        return messages

    def load_regions_from_db(self):
        """Загрузка геоданных регионов из базы данных с улучшенной обработкой"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, polygon FROM regions")
            regions_data = cursor.fetchall()

            for region in regions_data:
                try:
                    # Пытаемся распарсить полигон в разных форматах
                    polygon_data = None

                    # Попытка 1: как JSON
                    try:
                        polygon_data = json.loads(region['polygon'])
                    except:
                        pass

                    # Попытка 2: как Python literal
                    if not polygon_data:
                        try:
                            polygon_data = ast.literal_eval(region['polygon'])
                        except:
                            pass

                    # Попытка 3: как текст с координатами
                    if not polygon_data:
                        try:
                            # Формат: "55.7558,37.6176;55.7558,37.6176;..."
                            coords = []
                            for coord_pair in region['polygon'].split(';'):
                                if coord_pair.strip():
                                    lat, lon = coord_pair.split(',')
                                    coords.append((float(lon), float(lat)))
                            polygon_data = [coords]
                        except:
                            logging.error(f"Не удалось распарсить полигон для региона {region['name']}")
                            continue

                    if polygon_data and len(polygon_data) > 0:
                        # Преобразуем координаты в правильный порядок (долгота, широта)
                        main_polygon = polygon_data[0] if isinstance(polygon_data, list) else polygon_data

                        # Убедимся, что координаты в правильном порядке
                        formatted_coords = []
                        for coord in main_polygon:
                            if len(coord) >= 2:
                                # Если первое значение больше 90, это вероятно долгота
                                if abs(coord[0]) > 90 and abs(coord[1]) <= 90:
                                    formatted_coords.append((coord[0], coord[1]))  # долгота, широта
                                else:
                                    formatted_coords.append((coord[1], coord[0]))  # меняем местами

                        if len(formatted_coords) < 3:
                            logging.warning(
                                f"Полигон региона {region['name']} имеет недостаточно точек: {len(formatted_coords)}")
                            continue

                        polygon = Polygon(formatted_coords)
                        if not polygon.is_valid:
                            # Пытаемся исправить невалидный полигон
                            polygon = polygon.buffer(0)

                        prepped_polygon = prep(polygon)

                        self.regions.append({
                            'id': region['id'],
                            'name': region['name'],
                            'polygon': polygon,
                            'prepped_polygon': prepped_polygon
                        })
                except Exception as e:
                    logging.error(f"Ошибка обработки полигона для региона {region['name']}: {e}")
                    continue

            # Создаем пространственный индекс для быстрого поиска
            polygons = [region['polygon'] for region in self.regions]
            self.region_tree = STRtree(polygons)

            logging.info(f"Загружено {len(self.regions)} регионов из базы данных")
            return True

        except Exception as e:
            logging.error(f"Ошибка загрузки регионов из базы данных: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def parse_coordinates_universal(self, coord_str):
        """Универсальный парсинг координат с улучшенной обработкой форматов"""
        if not coord_str or not isinstance(coord_str, str):
            return None

        coord_str = coord_str.strip().upper()

        # Удаляем лишние символы (скобки, пробелы и т.д.)
        coord_str = re.sub(r'[^\dNSWE]', '', coord_str)

        # Различные форматы координат
        formats = [
            # Формат: DDMMSSNDDDMMSSW (440846N0430829W)
            r'(\d{6})([NS])(\d{7})([EW])',
            # Формат: DDMMSSNDDDMMSSW (440846N0430829W)
            r'(\d{6})([NS])(\d{6})([EW])',
            # Формат: DDMMNDDDMMW (4408N04308W)
            r'(\d{4})([NS])(\d{5})([EW])',
            # Формат: DDMMNDDDMMW (4408N04308W)
            r'(\d{4})([NS])(\d{4})([EW])',
            # Формат: DDMNDDDMW (448N0430W)
            r'(\d{3})([NS])(\d{4})([EW])',
            # Формат: DDMNDDDMW (448N0430W)
            r'(\d{3})([NS])(\d{3})([EW])',
        ]

        for fmt in formats:
            match = re.match(fmt, coord_str)
            if match:
                lat_str, lat_dir, lon_str, lon_dir = match.groups()
                break
        else:
            # Если не нашли соответствия стандартным форматам, пробуем альтернативные
            alt_match = re.match(r'(\d+)([NS])(\d+)([EW])', coord_str)
            if not alt_match:
                return None
            lat_str, lat_dir, lon_str, lon_dir = alt_match.groups()

        # Парсим широту
        lat_degrees, lat_minutes, lat_seconds = 0, 0, 0

        if len(lat_str) == 6:
            lat_degrees = int(lat_str[0:2])
            lat_minutes = int(lat_str[2:4])
            lat_seconds = int(lat_str[4:6])
        elif len(lat_str) == 5:
            lat_degrees = int(lat_str[0:2])
            lat_minutes = int(lat_str[2:4])
            lat_seconds = int(lat_str[4:5])
        elif len(lat_str) == 4:
            lat_degrees = int(lat_str[0:2])
            lat_minutes = int(lat_str[2:4])
        elif len(lat_str) == 3:
            lat_degrees = int(lat_str[0:2])
            lat_minutes = int(lat_str[2:3])
        else:
            lat_degrees = int(lat_str[0:2])
            if len(lat_str) > 2:
                lat_minutes = int(lat_str[2:])
            else:
                lat_minutes = 0

        # Парсим долготу
        lon_degrees, lon_minutes, lon_seconds = 0, 0, 0

        if len(lon_str) == 7:
            lon_degrees = int(lon_str[0:3])
            lon_minutes = int(lon_str[3:5])
            lon_seconds = int(lon_str[5:7])
        elif len(lon_str) == 6:
            lon_degrees = int(lon_str[0:3])
            lon_minutes = int(lon_str[3:5])
            lon_seconds = int(lon_str[5:6])
        elif len(lon_str) == 5:
            lon_degrees = int(lon_str[0:3])
            lon_minutes = int(lon_str[3:5])
        elif len(lon_str) == 4:
            if lon_str[0] == '0':
                lon_degrees = int(lon_str[0:3])
                lon_minutes = int(lon_str[3:4])
            else:
                lon_degrees = int(lon_str[0:2])
                lon_minutes = int(lon_str[2:4])
        else:
            lon_degrees = int(lon_str[0:3])
            if len(lon_str) > 3:
                lon_minutes = int(lon_str[3:])
            else:
                lon_minutes = 0

        # Преобразуем в десятичные градусы
        latitude = lat_degrees + (lat_minutes / 60) + (lat_seconds / 3600)
        if lat_dir == 'S':
            latitude = -latitude

        longitude = lon_degrees + (lon_minutes / 60) + (lon_seconds / 3600)
        if lon_dir == 'W':
            longitude = -longitude

        return {
            'original': coord_str,
            'latitude': round(latitude, 6),
            'longitude': round(longitude, 6)
        }

    def find_region(self, lat: float, lon: float) -> Optional[str]:
        """Поиск региона по координатам с использованием пространственного индекса"""
        if lat is None or lon is None or not self.regions or not self.region_tree:
            return None

        point = Point(lon, lat)

        try:
            # Используем пространственный индекс для быстрого поиска
            possible_indices = self.region_tree.query(point)

            for idx in possible_indices:
                region = self.regions[idx]
                if region['prepped_polygon'].contains(point):
                    return [region['id'], region['name']]

        except Exception as e:
            logging.error(f"Ошибка при поиске региона: {e}")

        return None

    def parse_quantity(self, typ_str: str) -> int:
        """Извлечение количества БПЛА из строки TYP"""
        if not typ_str or not isinstance(typ_str, str):
            return 1

        # Ищем паттерн: число перед BLA
        match = re.search(r'(\d+)BLA', typ_str, re.IGNORECASE)
        if match:
            return int(match.group(1))
        else:
            # Если нет числа, то по умолчанию 1
            return 1

    def extract_sid(self, text: str) -> Optional[str]:
        """Извлечение SID с валидацией как в PHP коде"""
        if not text or not isinstance(text, str):
            return None

        # Более строгое регулярное выражение
        match = re.search(r'SID\/(\d{7,15})\b', text)
        if match:
            sid = match.group(1)

            # Проверяем, что SID состоит только из цифр и имеет разумную длину
            if sid.isdigit() and len(sid) >= 7 and len(sid) <= 15:
                return sid

        return None

    def extract_aircraft_type(self, text: str) -> Dict[str, Any]:
        """Извлечение типа воздушного судна с информацией как в PHP коде"""
        type_codes = {
            'BLA': 'Беспилотный летательный аппарат (дрон)',
            'AER': 'Самолет',
            'HEL': 'Вертолет',
            'SHAR': 'Аэростат',
            'GLI': 'Планер',
            'UAV': 'Беспилотный летательный аппарат',
            'GYR': 'Автожир',
            'ULM': 'Сверхлегкий летательный аппарат'
        }

        if not text or not isinstance(text, str):
            return {'code': 'UNKNOWN', 'quantity': 1}

        # Ищем паттерн TYP/ с возможными цифрами перед типом
        match = re.search(r'TYP\/(\d*)([A-Z]{3,4})', text)
        if match:
            quantity = int(match.group(1)) if match.group(1) else 1
            type_code = match.group(2)
            type_description = type_codes.get(type_code, 'Неизвестный тип воздушного судна')

            return {
                'code': type_code,
                'description': type_description,
                'quantity': quantity
            }

        return {'code': 'UNKNOWN', 'quantity': 1}

    def extract_flight_data(self, messages: Dict[str, str]) -> Dict[str, Any]:
        """Извлечение данных о полете из всех источников с улучшенным парсингом"""
        result = {
            'start_coordinates': None,
            'end_coordinates': None,
            'raw_data': {}
        }

        # Обрабатываем координаты из SHR
        if messages.get('shr') and isinstance(messages['shr'], str):
            shr = messages['shr']

            # Ищем DEP координаты
            dep_match = re.search(r'DEP\/([0-9NSWE]+)', shr)
            if dep_match:
                dep_coords = self.parse_coordinates_universal(dep_match.group(1))
                result['raw_data']['shr_dep'] = dep_coords
                result['start_coordinates'] = dep_coords

            # Ищем DEST координаты
            dest_match = re.search(r'DEST\/([0-9NSWE]+)', shr)
            if dest_match:
                dest_coords = self.parse_coordinates_universal(dest_match.group(1))
                result['raw_data']['shr_dest'] = dest_coords
                result['end_coordinates'] = dest_coords

            # Ищем координаты в других форматах
            if not result['start_coordinates']:
                # Формат: DEP-координаты-...
                dep_alt_match = re.search(r'DEP-([0-9NSWE]+)', shr)
                if dep_alt_match:
                    dep_coords = self.parse_coordinates_universal(dep_alt_match.group(1))
                    result['raw_data']['shr_dep_alt'] = dep_coords
                    result['start_coordinates'] = dep_coords

        # Обрабатываем координаты из DEP
        if messages.get('dep') and isinstance(messages['dep'], str):
            dep = messages['dep']

            # Ищем ADEPZ координаты
            adepz_match = re.search(r'-ADEPZ\s+([0-9NSWE]+)', dep)
            if adepz_match:
                adepz_coords = self.parse_coordinates_universal(adepz_match.group(1))
                result['raw_data']['dep_adepz'] = adepz_coords
                if not result['start_coordinates']:
                    result['start_coordinates'] = adepz_coords

            # Ищем координаты в других форматах DEP
            coord_matches = re.findall(r'[NS]\d+[EW]\d+', dep)
            for coord_match in coord_matches:
                coords = self.parse_coordinates_universal(coord_match)
                if coords and not result['start_coordinates']:
                    result['start_coordinates'] = coords
                    result['raw_data']['dep_auto'] = coords
                    break

        # Обрабатываем координаты из ARR
        if messages.get('arr') and isinstance(messages['arr'], str):
            arr = messages['arr']

            # Ищем ADARRZ координаты
            adarrz_match = re.search(r'-ADARRZ\s+([0-9NSWE]+)', arr)
            if adarrz_match:
                adarrz_coords = self.parse_coordinates_universal(adarrz_match.group(1))
                result['raw_data']['arr_adarrz'] = adarrz_coords
                if not result['end_coordinates']:
                    result['end_coordinates'] = adarrz_coords

            # Ищем координаты в других форматах ARR
            coord_matches = re.findall(r'[NS]\d+[EW]\d+', arr)
            for coord_match in coord_matches:
                coords = self.parse_coordinates_universal(coord_match)
                if coords and not result['end_coordinates']:
                    result['end_coordinates'] = coords
                    result['raw_data']['arr_auto'] = coords
                    break

        return result

    def parse_time_string(self, time_str):
        """Парсинг строки времени в объект time"""
        if not time_str or not isinstance(time_str, str):
            return None

        try:
            # Удаляем все нецифровые символы
            digits = re.sub(r'\D', '', time_str)

            if len(digits) == 4:
                # Формат HHMM
                hours = int(digits[:2])
                minutes = int(digits[2:4])
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    return time(hours, minutes)
            elif len(digits) == 3:
                # Формат HMM
                hours = int(digits[0])
                minutes = int(digits[1:3])
                if 0 <= hours < 24 and 0 <= minutes < 60:
                    return time(hours, minutes)
            elif len(digits) == 2:
                # Формат MM
                minutes = int(digits)
                if 0 <= minutes < 60:
                    return time(0, minutes)
            elif len(digits) == 1:
                # Формат M
                minutes = int(digits)
                if 0 <= minutes < 60:
                    return time(0, minutes)
        except (ValueError, TypeError):
            pass

        return None

    def parse_date_string(self, date_str):
        """Парсинг строки дата в объект date"""
        if not date_str or not isinstance(date_str, str):
            return None

        try:
            # Удаляем все нецифровые символы
            digits = re.sub(r'\D', '', date_str)

            if len(digits) == 6:
                # Формат DDMMYY
                day = int(digits[:2])
                month = int(digits[2:4])
                year = 2000 + int(digits[4:6])
                if 1 <= day <= 31 and 1 <= month <= 12:
                    return date(year, month, day)
            elif len(digits) == 4:
                # Формат DDMM - используем текущий год
                day = int(digits[:2])
                month = int(digits[2:4])
                year = datetime.now().year
                if 1 <= day <= 31 and 1 <= month <= 12:
                    return date(year, month, day)
        except (ValueError, TypeError):
            pass

        return None

    def extract_flight_times(self, messages: Dict[str, str]) -> Dict[str, Any]:
        """Извлечение времени полета из всех источников"""
        result = {
            'shr': {},
            'dep': {},
            'arr': {},
            'final': {}
        }

        # Обрабатываем SHR
        if messages.get('shr') and isinstance(messages['shr'], str):
            shr = messages['shr']

            # Ищем временные метки ZZZZ
            if re.search(r'-ZZZZ(\d{4})', shr):
                matches = re.findall(r'-ZZZZ(\d{4})', shr)
                result['shr']['zzzz_times'] = matches

                if len(matches) >= 2:
                    result['shr']['end_time'] = self.parse_time_string(matches[1])
                    result['shr']['start_time'] = self.parse_time_string(matches[0])
                elif len(matches) == 1:
                    result['shr']['start_time'] = self.parse_time_string(matches[0])

            # Ищем дату полета DOF
            if re.search(r'DOF/(\d{6})', shr):
                match = re.search(r'DOF/(\d{6})', shr)
                date_str = match.group(1)
                year = int(date_str[0:2]) + 2000
                month = int(date_str[2:4])
                day = int(date_str[4:6])
                try:
                    flight_date = datetime(year, month, day)
                    result['shr']['flight_date'] = flight_date.strftime('%Y-%m-%d')
                except ValueError:
                    result['shr']['flight_date'] = None

        # Обрабатываем DEP
        if messages.get('dep') and isinstance(messages['dep'], str):
            dep = messages['dep']

            # Время вылета
            if re.search(r'-ATD\s+(\d{4})', dep):
                match = re.search(r'-ATD\s+(\d{4})', dep)
                result['dep']['atd_time'] = self.parse_time_string(match.group(1))

            # Дата вылета
            if re.search(r'-ADD\s+(\d{6})', dep):
                match = re.search(r'-ADD\s+(\d{6})', dep)
                result['dep']['add_date'] = self.parse_date_string(match.group(1))

        # Обрабатываем ARR
        if messages.get('arr') and isinstance(messages['arr'], str):
            arr = messages['arr']

            # Время прибытия
            if re.search(r'-ATA\s+(\d{4})', arr):
                match = re.search(r'-ATA\s+(\d{4})', arr)
                result['arr']['ata_time'] = self.parse_time_string(match.group(1))

            # Дата прибытия
            if re.search(r'-ADA\s+(\d{6})', arr):
                match = re.search(r'-ADA\s+(\d{6})', arr)
                result['arr']['ada_date'] = self.parse_date_string(match.group(1))

        # Формируем финальный результат
        result['final'] = {
            'start_time_shr': result['shr'].get('start_time'),
            'end_time_shr': result['shr'].get('end_time'),
            'date_shr': result['shr'].get('flight_date'),
            'start_time_dep': result['dep'].get('atd_time'),
            'date_dep': result['dep'].get('add_date'),
            'end_time_arr': result['arr'].get('ata_time'),
            'date_arr': result['arr'].get('ada_date'),
        }

        # Заполняем отсутствующие значения
        final = result['final']

        # Для дат
        if not final['date_dep'] and final['date_arr']:
            final['date_dep'] = final['date_arr']
        elif not final['date_arr'] and final['date_dep']:
            final['date_arr'] = final['date_dep']
        elif not final['date_dep'] and not final['date_arr'] and final['date_shr']:
            final['date_dep'] = final['date_shr']
            final['date_arr'] = final['date_shr']

        # Для времени
        if not final['start_time_dep'] and final['end_time_arr']:
            final['start_time_dep'] = final['end_time_arr']
        elif not final['end_time_arr'] and final['start_time_dep']:
            final['end_time_arr'] = final['start_time_dep']
        elif not final['start_time_dep'] and final['start_time_shr']:
            final['start_time_dep'] = final['start_time_shr']
        elif not final['end_time_arr'] and final['end_time_shr']:
            final['end_time_arr'] = final['end_time_shr']

        return result



    def extract_operator_info(self, text: str) -> Dict[str, Any]:
        """Извлечение информации об операторе"""
        if not text or not isinstance(text, str):
            return {'operator': None, 'phone_number': None}

        result = {'operator': None, 'phone_number': None}

        # Поиск оператора
        operator_patterns = [
            r'OPR\/([^\s]+)',
            r'OPERATOR\/([^\s]+)',
            r'RMK\/.*?OPR[:\s]*([^\n]+)',
            r'RMK\/.*?OPERATOR[:\s]*([^\n]+)',
        ]

        for pattern in operator_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result['operator'] = match.group(1).strip()
                break

        # Поиск номера телефона
        phone_patterns = [
            r'TEL\/([^\s]+)',
            r'PHONE\/([^\s]+)',
            r'RMK\/.*?TEL[:\s]*([^\n]+)',
            r'RMK\/.*?PHONE[:\s]*([^\n]+)',
            r'(\+7[\d\(\)\s-]{10,15})',  # Российские номера
            r'(\+?[\d\(\)\s-]{10,15})',  # Международные номера
        ]

        for pattern in phone_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result['phone_number'] = re.sub(r'\D', '', match.group(1))  # Оставляем только цифры
                break

        return result

    def extract_flight_number(self, text: str) -> Optional[str]:
        """Извлечение номера рейса"""
        if not text or not isinstance(text, str):
            return None

        patterns = [
            r'FLIGHT\/([^\s]+)',
            r'FLC\/([^\s]+)',
            r'CALLSIGN\/([^\s]+)',
            r'(\b[A-Z]{2}\d{3,4}\b)',  # Пример: SU1234
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def extract_registration(self, text: str) -> Optional[str]:
        """Извлечение регистрационного номера"""
        if not text or not isinstance(text, str):
            return None

        patterns = [
            r'REG\/([^\s]+)',
            r'REGISTRATION\/([^\s]+)'
            r'(\b[A-Z]{1,2}-\d{4,5}\b)',  # Пример: RA-12345
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def extract_altitude_info(self, text: str) -> Optional[str]:
        """Извлечение информации о высоте"""
        if not text or not isinstance(text, str):
            return None

        patterns = [
            r'ALT\/([^\s]+)',
            r'ALTITUDE\/([^\s]+)',
            r'LEVEL\/([^\s]+)',
            r'FL\/([^\s]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def extract_remarks(self, text: str) -> Optional[str]:
        """Извлечение примечаний"""
        if not text or not isinstance(text, str):
            return None

        match = re.search(r'RMK\/([^\n]+)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return None

    def extract_eet_info(self, text: str) -> Optional[str]:
        """Извлечение расчетного времени полета (EET) и преобразование в минуты или читаемый формат"""
        if not text or not isinstance(text, str):
            return None
        match = re.search(r'EET/(\d{4})', text, re.IGNORECASE)
        if match:
            eet_str = match.group(1)
            try:
                hours = int(eet_str[:2])
                minutes = int(eet_str[2:4])
                total_minutes = hours * 60 + minutes
                return f"{hours:02d}:{minutes:02d} ({total_minutes} мин)"
            except (ValueError, IndexError):
                return eet_str.strip()
        return None

    def calculate_duration(self, start_time, end_time):
        """Расчет длительности полета в минутах"""
        if not start_time or not end_time:
            return None
        try:
            # Если start_time и end_time - объекты time
            if isinstance(start_time, time) and isinstance(end_time, time):
                start_dt = datetime.combine(date.today(), start_time)
                end_dt = datetime.combine(date.today(), end_time)
                # Если время окончания меньше времени начала, предполагаем, что полет закончился на следующий день
                if end_dt < start_dt:
                    end_dt = end_dt.replace(day=end_dt.day + 1)
                duration = end_dt - start_dt
                return int(duration.total_seconds() / 60)
        except Exception as e:
            logging.error(f"Ошибка расчета длительности: {e}")
        return None

    def process_flights(self, data, limit: int = None, batch_size: int = 1000):
        """Основной метод обработки данных о полетах"""


        if not self.connection:
            logging.error("Не инициализировано соединение с БД")
            return


        try:
            total_count = len(data)

            if limit:
                total_count = min(limit, total_count)
                logging.info(f"Обработка ограничена {limit} записями")

            self.total_records_in_file = total_count
            logging.info(f"Всего записей для обработки: {total_count}")
            self.update_progress(0, total_count, f"Всего записей для обработки: {total_count}")

            # Создание таблицы для результатов
            self.create_results_table()

            processed = 0
            start_time = time_module.time()
            batch_values = []  # Список для накопления значений батча

            for i, row in enumerate(data):
                if limit and processed >= limit:
                    break

                try:
                    # Обновляем прогресс каждые 10000 записей
                    if i % 5000 == 0:
                        self.update_progress(i, total_count + 1, "Обработка записей")

                    # Обрабатываем запись и получаем значения для вставки
                    values = self.process_single_flight(row)
                    if values:
                        # Добавляем имя файла к значениям
                        values_with_filename = values + (self.current_filename,)
                        batch_values.append(values_with_filename)
                        processed += 1

                    # Если накопился батч, вставляем
                    if len(batch_values) >= batch_size:
                        self.save_batch(batch_values)
                        batch_values = []
                        logging.info(f"Вставлено {processed} записей")

                except Exception as e:
                    logging.error(f"Ошибка обработки записи {i}: {e}")
                    continue

            # Вставляем оставшиеся записи
            if batch_values:
                self.save_batch(batch_values)

            # Обновляем прогресс до 100%
            self.update_progress(total_count, total_count, "Завершение обработки")

            total_time = time_module.time() - start_time
            logging.info(
                f"Обработка завершена. Время: {total_time:.1f} сек, скорость: {processed / total_time:.1f} записей/сек")

            # Логируем статистику заполненности полей
            self.log_field_statistics()

        except Exception as e:
            error_msg = f"Ошибка при обработке полетов: {e}"
            logging.error(error_msg)
            if self.connection:
                self.connection.rollback()

    def save_batch(self, batch_values):
        """Массовая вставка батча данных"""
        if not batch_values:
            return

        try:
            cursor = self.connection.cursor()
            query = """
                INSERT IGNORE INTO processed_flights 
                (source_id, sheet_name, flight_id, flight_number, aircraft_type, region_id, departure_region, arrival_region, 
                 duration_min, operator, registration, departure_coords, arrival_coords,
                 departure_lat, departure_lon, arrival_lat, arrival_lon, dof_date, atd_time, ata_time,
                 eet_info, remarks, center_es_orvd, altitude_info, phone_number, quantity, filename)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # query = """
            #     INSERT INTO processed_flights
            #     (source_id, sheet_name, flight_id, flight_number, aircraft_type, region_id, departure_region, arrival_region,
            #      duration_min, operator, registration, departure_coords, arrival_coords,
            #      departure_lat, departure_lon, arrival_lat, arrival_lon, dof_date, atd_time, ata_time,
            #      eet_info, remarks, center_es_orvd, altitude_info, phone_number, quantity, filename)
            #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            # """
            cursor.executemany(query, batch_values)
            self.connection.commit()
            logging.info(f"Вставлено {len(batch_values)} записей")
        except Exception as e:
            # Логируем ошибки усечения данных
            if "Data truncated" in str(e):
                logging.error(f"Ошибка усечения данных: {e}")
                # Пробуем вставить по одной записи, чтобы найти проблемную
                for i, values in enumerate(batch_values):
                    try:
                        cursor.execute(query, values)
                    except Exception as e2:
                        logging.error(f"Ошибка вставки записи {i}: {e2}")
                        logging.error(f"Проблемные значения: {values}")
            else:
                logging.error(f"Ошибка массовой вставки: {e}")
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()

    def create_results_table(self):
        """Создание таблицы для результатов обработки"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES LIKE 'processed_flights'")
            if cursor.fetchone():
                # Проверяем наличие поля filename
                cursor.execute("SHOW COLUMNS FROM processed_flights LIKE 'filename'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE processed_flights ADD COLUMN filename VARCHAR(255)")
                    self.connection.commit()
                    logging.info("Добавлено поле filename в таблицу processed_flights")
                else:
                    logging.info("Таблица processed_flights уже существует и содержит поле filename")
                return

            cursor.execute("""
                           CREATE TABLE `processed_flights` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `source_id` varchar(255) DEFAULT NULL COMMENT 'ID из исходных данных',
                  `sheet_name` varchar(100) DEFAULT NULL COMMENT 'Название листа в Excel',
                  `flight_id` varchar(255) DEFAULT NULL COMMENT 'Идентификатор полета (SID)',
                  `flight_number` varchar(100) DEFAULT NULL COMMENT 'Номер рейса',
                  `aircraft_type` varchar(100) DEFAULT NULL COMMENT 'Тип воздушного судна',
                  `departure_region` varchar(100) DEFAULT NULL COMMENT 'Регион вылета',
                  `arrival_region` varchar(100) DEFAULT NULL COMMENT 'Регион прибытия',
                  `duration_min` int(11) DEFAULT NULL COMMENT 'Длительность полета в минутах',
                  `operator` varchar(255) DEFAULT NULL COMMENT 'Оператор (ФИО или организация)',
                  `registration` varchar(255) DEFAULT NULL COMMENT 'Регистрационный номер ВС',
                  `departure_coords` varchar(100) DEFAULT NULL COMMENT 'Координаты вылета в исходном формате',
                  `arrival_coords` varchar(100) DEFAULT NULL COMMENT 'Координаты прибытия в исходном формате',
                  `departure_lat` float DEFAULT NULL COMMENT 'Широта вылета в десятичных градусах',
                  `departure_lon` float DEFAULT NULL COMMENT 'Долгота вылета в десятичных градусах',
                  `arrival_lat` float DEFAULT NULL COMMENT 'Широта прибытия в десятичных градусах',
                  `arrival_lon` float DEFAULT NULL COMMENT 'Долгота прибытия в десятичных градусах',
                  `dof_date` date DEFAULT NULL COMMENT 'Дата полета',
                  `atd_time` time DEFAULT NULL COMMENT 'Время вылета',
                  `ata_time` time DEFAULT NULL COMMENT 'Время прибытия',
                  `eet_info` varchar(100) DEFAULT NULL COMMENT 'Расчетное время полета',
                  `remarks` text COMMENT 'Примечания (RMK)',
                  `center_es_orvd` varchar(100) DEFAULT NULL COMMENT 'Центр ЕС ОрВД',
                  `altitude_info` varchar(100) DEFAULT NULL COMMENT 'Информация о высоте',
                  `phone_number` varchar(255) DEFAULT NULL COMMENT 'Номер телефона оператора',
                  `quantity` int(11) DEFAULT NULL COMMENT 'Количество БПЛА',
                  `processed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `filename` varchar(255) DEFAULT NULL COMMENT 'Имя исходного файла',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `unique_flight` (`source_id`,`sheet_name`,`flight_id`),
                  KEY `idx_departure_region` (`departure_region`),
                  KEY `idx_arrival_region` (`arrival_region`),
                  KEY `idx_aircraft_type` (`aircraft_type`),
                  KEY `idx_operator` (`operator`(20)),
                  KEY `idx_dof_date` (`dof_date`),
                  KEY `idx_sheet_name` (`sheet_name`),
                  KEY `idx_departure_coords` (`departure_lat`,`departure_lon`)
                ) ENGINE=InnoDB AUTO_INCREMENT=334557 DEFAULT CHARSET=utf8mb4 COMMENT='Таблица обработанных данных о полетах БПЛА';
            """)
            self.connection.commit()
            logging.info("Таблица результатов создана")
        except Exception as e:
            logging.error(f"Ошибка создания таблицы результатов: {e}")
        finally:
            if cursor:
                cursor.close()

    def log_field_statistics(self):
        """Логирование статистики заполненности полей"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            fields_to_check = [
                'operator',
                'registration',
                'quantity',
                'flight_id',
                'flight_number',
                'aircraft_type',
                'departure_region',
                'arrival_region',
                'duration_min',
                'departure_coords',
                'arrival_coords',
                'dof_date',
                'atd_time',
                'ata_time'
            ]

            stats = {}
            cursor.execute("SELECT COUNT(*) as count FROM processed_flights")
            total_records = cursor.fetchone()['count']

            for field in fields_to_check:
                cursor.execute(f"SELECT COUNT(*) as count FROM processed_flights WHERE {field} IS NOT NULL")
                non_null_count = cursor.fetchone()['count']
                stats[field] = {
                    'non_null': non_null_count,
                    'null': total_records - non_null_count,
                    'percentage': (non_null_count / total_records * 100) if total_records > 0 else 0
                }

            logging.info("=== СТАТИСТИКА ЗАПОЛНЕННОСТИ ПОЛЕЙ ===")
            self.update_progress(99, 100, f"СТАТИСТИКА ЗАПОЛНЕННОСТИ ПОЛЕЙ ")
            for field, data in stats.items():
                logging.info(f"{field}: {data['non_null']}/{total_records} ({data['percentage']:.1f}%) заполнено")
                self.update_progress(99, 100,f"{field}: {data['non_null']}/{total_records} ({data['percentage']:.1f}%) заполнено")

        except Exception as e:
            logging.error(f"Ошибка при получении статистики: {e}")
        finally:
            if cursor:
                cursor.close()

    def process_single_flight(self, row: Dict[str, Any]):
        """Обработка одиночного полета и возврат значений для вставки"""
        try:
            # Извлекаем сообщения
            messages = self.extract_messages(row)

            # Если нет ни одного сообщения, пропускаем
            if not any(messages.values()):
                logging.debug("Не найдено ни одного сообщения (SHR, DEP, ARR) для обработки")
                return None

            # Извлекаем SID
            sid = None
            if messages['shr']:
                sid = self.extract_sid(messages['shr'])
            if not sid and messages['dep']:
                sid = self.extract_sid(messages['dep'])
            if not sid and messages['arr']:
                sid = self.extract_sid(messages['arr'])

            # Извлекаем тип воздушного судна и количество
            aircraft_info = None
            if messages['shr']:
                aircraft_info = self.extract_aircraft_type(messages['shr'])
            if not aircraft_info and messages['dep']:
                aircraft_info = self.extract_aircraft_type(messages['dep'])
            if not aircraft_info and messages['arr']:
                aircraft_info = self.extract_aircraft_type(messages['arr'])

            if not aircraft_info:
                aircraft_info = {'code': 'UNKNOWN', 'quantity': 1}

            # Извлекаем координаты
            flight_data = self.extract_flight_data(messages)
            start_coords = flight_data.get('start_coordinates')
            end_coords = flight_data.get('end_coordinates')

            # Извлекаем время полета
            flight_times = self.extract_flight_times(messages)
            final_times = flight_times.get('final', {})

            # Рассчитываем длительность полета
            duration_min = self.calculate_duration(
                final_times.get('start_time_shr') or final_times.get('start_time_dep'),
                final_times.get('end_time_shr') or final_times.get('end_time_arr')
            )

            # # Определяем регионы
            # departure_region = None
            # arrival_region = None
            # region_id = 0
            #
            # if end_coords:
            #     [region_id, arrival_region] = self.find_region(end_coords['latitude'], end_coords['longitude'])
            #
            # if start_coords:
            #     [region_id, departure_region] = self.find_region(start_coords['latitude'], start_coords['longitude'])
            region_id = 0
            departure_region = None
            arrival_region = None

            if end_coords:
                result = self.find_region(end_coords['latitude'], end_coords['longitude'])
                if result:
                    region_id, arrival_region = result

            if start_coords:
                result = self.find_region(start_coords['latitude'], start_coords['longitude'])
                if result:
                    region_id, departure_region = result

            # Извлекаем дополнительную информацию
            operator_info = {'operator': None, 'phone_number': None}
            flight_number = None
            registration = None
            altitude_info = None
            remarks = None
            eet_info = None

            # Ищем информацию во всех сообщениях
            for msg_type, msg_text in messages.items():
                if msg_text:
                    # Оператор и телефон
                    op_info = self.extract_operator_info(msg_text)
                    if op_info['operator'] and not operator_info['operator']:
                        operator_info['operator'] = op_info['operator']
                    if op_info['phone_number'] and not operator_info['phone_number']:
                        operator_info['phone_number'] = op_info['phone_number']

                    # Номер рейса
                    if not flight_number:
                        flight_number = self.extract_flight_number(msg_text)

                    # Регистрационный номер
                    if not registration:
                        registration = self.extract_registration(msg_text)

                    # Информация о высоте
                    if not altitude_info:
                        altitude_info = self.extract_altitude_info(msg_text)

                    # Примечания
                    if not remarks:
                        remarks = self.extract_remarks(msg_text)

                    # Расчетное время полета
                    if not eet_info:
                        eet_info = self.extract_eet_info(msg_text)

            # Получаем ID из исходных данных
            source_id = row.get('source_id')

            # Формируем кортеж значений для вставки
            values = (
                str(source_id)[:255] if source_id else None,
                row.get('sheet_name'),
                sid,
                flight_number,
                aircraft_info['code'],
                region_id,
                departure_region,
                arrival_region,
                duration_min,
                operator_info['operator'],
                registration,
                start_coords['original'] if start_coords else None,
                end_coords['original'] if end_coords else None,
                start_coords['latitude'] if start_coords else None,
                start_coords['longitude'] if start_coords else None,
                end_coords['latitude'] if end_coords else None,
                end_coords['longitude'] if end_coords else None,
                final_times.get('date_shr') or final_times.get('date_dep') or final_times.get('date_arr'),
                final_times.get('start_time_shr') or final_times.get('start_time_dep'),
                final_times.get('end_time_shr') or final_times.get('end_time_arr'),
                eet_info,
                remarks,
                row.get('centr_es_orvd') or row.get('Центр ЕС ОрВД'),
                altitude_info,
                operator_info['phone_number'],
                aircraft_info['quantity']
            )

            return values

        except Exception as e:
            logging.error(f"Ошибка обработки записи: {e}")
            return None

    def close_connection(self):
        """Закрытие соединения с БД"""
        if self.connection:
            self.connection.close()
            logging.info("Соединение с базой данных закрыто")

    def process_all_files(self):
        """Совместимость: просто вызывает обработку непроцессированных файлов."""
        self.process_unprocessed_files()



def main():
    """Функция для запуска модуля отдельно"""
    processor = FlightDataProcessor()
    processor.process_all_files()


if __name__ == "__main__":
    main()