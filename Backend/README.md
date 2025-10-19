# ✈️ АЭРОМЕТР

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

**Автоматизированная облачная система для сбора, обработки и анализа данных о полетах БПЛА в регионах России**

[🌐 Демо-сайт](https://aerometr.ru) • [📊 Презентация](https://docs.google.com/presentation/d/1tS-MUPT5ISglaNvYg3ztEVZ49lHhbtIfs-_1oyVkrAg/edit?usp=sharing) • [🏗️ Архитектура](https://aerometr.ru/files/docs/drawio.html)

</div>

---

## 📋 Оглавление

- [О проекте](#-о-проекте)
- [Ключевые возможности](#-ключевые-возможности)
- [Архитектура системы](#-архитектура-системы)
- [Технологический стек](#-технологический-стек)
- [Быстрый старт](#-быстрый-старт)
- [Структура проекта](#-структура-проекта)
- [Модули системы](#-модули-системы)
- [API и управление](#-api-и-управление)
- [База данных](#-база-данных)
- [Конфигурация](#-конфигурация)
- [Использование](#-использование)
- [Производительность](#-производительность)
- [Разработка](#-разработка)

---

## 🎯 О проекте

**АЭРОМЕТР** — комплексная система автоматизированной обработки и анализа полетных данных беспилотных авиационных систем (БПЛА) на территории Российской Федерации.

Система разработана в рамках поддержки национального проекта **«Беспилотные авиационные системы» (2024-2030 гг.)**, который предусматривает:
- 🏗️ Создание **290 посадочных площадок** к 2030 году
- 💰 Финансирование в размере **696 млрд рублей**
- 📡 Развитие инфраструктуры беспилотной авиации

### Основная задача

Сбор, агрегация и интеллектуальный анализ данных о полетах БПЛА из множества источников для:
- Оптимизации размещения инфраструктуры
- Прогнозирования полетной активности
- Анализа региональной динамики
- Поддержки принятия управленческих решений

---

## ⚡ Ключевые возможности

### 📊 Анализ данных
- **Автоматический парсинг** Excel-файлов с FTP-сервера
- **Геопривязка** полетов к официальным границам субъектов РФ
- **Расчет длительности** и интенсивности полетов
- **Агрегация статистики** по регионам и временным периодам

### 🗺️ Пространственный анализ
- Генерация **квадратных** и **гексагональных сеток** (H3)
- Расчет **плотности полетов** на территории
- Анализ **запретных зон** и ограничений
- Оптимальное **размещение площадок** для БПЛА

### 📈 Прогнозирование
- Генерация **прогнозов полетной активности**
- Анализ **трендов** по регионам
- Предсказание **пиковых нагрузок**

### 🛰️ Сбор данных в реальном времени
- Интеграция с **OpenSky Network**
- Отслеживание **активных воздушных судов**
- Обновление данных **каждые 600 секунд**
- Автоматическая **очистка устаревших данных** (24 часа)

### 🤖 AI-генерация
- Генерация изображений регионов через **FusionBrain AI**
- Альтернативная генерация через **GigaChat**
- Автоматическое создание визуального контента

### 🔧 Управление и мониторинг
- **Web-интерфейс** для управления системой
- **REST API** для интеграции
- **Мониторинг фоновых процессов**
- **Автоматическое резервное копирование**

---

## 🏗️ Архитектура системы

```
┌─────────────────────────────────────────────────────────────────┐
│                         ВНЕШНИЕ ИСТОЧНИКИ                        │
├─────────────┬──────────────┬──────────────┬─────────────────────┤
│ FTP Сервер  │ OpenSky API  │ Overpass API │ AI API (Fusion/Giga)│
│ (Excel)     │ (Самолеты)   │ (Границы)    │ (Изображения)       │
└─────┬───────┴──────┬───────┴──────┬───────┴─────────┬───────────┘
      │              │              │                 │
      v              v              v                 v
┌─────────────────────────────────────────────────────────────────┐
│                       СЛОЙ ОБРАБОТКИ                            │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│   Parser     │   Aircraft   │ OpenStreetMap│   ImageGenerator   │
│   Module     │   Module     │    Module    │      Module        │
└──────┬───────┴──────┬───────┴──────┬───────┴─────────┬──────────┘
       │              │              │                 │
       v              v              v                 v
┌─────────────────────────────────────────────────────────────────┐
│                      БИЗНЕС-ЛОГИКА                              │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│   Region     │     Grid     │  Area BPLA   │   Prediction       │
│   Stats      │  Generator   │  Generator   │     Module         │
└──────┬───────┴──────┬───────┴──────┬───────┴─────────┬──────────┘
       │              │              │                 │
       v              v              v                 v
┌─────────────────────────────────────────────────────────────────┐
│                    ХРАНИЛИЩЕ ДАННЫХ (MySQL)                     │
├─────────────────────────────────────────────────────────────────┤
│ • processed_flights  • grid_hexagon    • area_bpla             │
│ • aircraft          • grid_square      • predictions           │
│ • regions           • region_stats     • processed_files       │
└─────────────────────────────────────────────────────────────────┘
       │                                                   ^
       v                                                   │
┌─────────────────────────────────────────────────────────────────┐
│                      API & WEB ИНТЕРФЕЙС                        │
├─────────────────────────────────────────────────────────────────┤
│  Flask REST API  │  Web Dashboard  │  DataLens Integration    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Технологический стек

### Backend

| Технология | Назначение |
|-----------|-----------|
| **Python 3.8+** | Основная логика обработки данных |
| **Flask** | REST API и веб-интерфейс |
| **MySQL 8.0+** | Реляционная база данных |
| **Shapely** | Обработка геометрических объектов |
| **H3** | Гексагональная иерархическая геопространственная индексация |
| **Pandas** | Обработка табличных данных |
| **NumPy** | Численные вычисления |

### Внешние сервисы

| API | Описание |
|-----|----------|
| **OpenSky Network** | Данные о воздушных судах в реальном времени |
| **Overpass API (OSM)** | Геоданные и границы регионов |
| **FusionBrain AI** | Генерация изображений (Kandinsky) |
| **GigaChat** | Альтернативная генерация изображений |
| **Yandex DataLens** | Визуализация и дашборды |

### Библиотеки и зависимости

```
mysql-connector-python  # Коннектор MySQL
requests               # HTTP-запросы
shapely               # Геометрия
schedule              # Планировщик задач
rtree                 # Пространственные индексы
h3                    # Гексагональные сетки
pandas                # Обработка данных
openpyxl              # Работа с Excel
beautifulsoup4        # Парсинг HTML
osm2geojson           # Конвертация OSM
PyJWT                 # JWT токены
Flask                 # Web-фреймворк
numpy                 # Вычисления
```

---

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8 или выше
- MySQL 8.0 или выше
- Git
- 4+ ГБ RAM
- Доступ к интернету (для API)

### Установка

#### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/aerometr.git
cd aerometr
```

#### 2. Создание виртуального окружения

**Linux/MacOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 4. Настройка базы данных

```sql
CREATE DATABASE aerometr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Импортируйте схему базы данных (если есть SQL-дамп):
```bash
mysql -u username -p aerometr < database/schema.sql
```

#### 5. Конфигурация

Создайте файл `settings.py` (или отредактируйте существующий):

```python
# Конфигурация базы данных
DB_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '3306',
    'database': 'aerometr',
    'raise_on_warnings': True,
    'connect_timeout': 30000,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# API ключи FusionBrain
FUSION_BRAIN = {
    'api_key': 'your_api_key',
    'secret_key': 'your_secret_key'
}

# API ключи GigaChat
GIGACHAT_CREDENTIALS = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret'
}

# Настройки FTP
FTP_CONFIG = {
    'host': 'ftp.example.com',
    'username': 'your_username',
    'password': 'your_password',
    'remote_dir': '/path/to/files/',
}
```

#### 6. Запуск системы

**Фоновый режим (рекомендуется):**
```bash
python main.py
```

**Web-интерфейс управления:**
```bash
python app.py
```

Откройте браузер: `http://localhost:5000`

---

## 📁 Структура проекта

```
aerometr/
│
├── aircraft/                    # Модуль сбора данных о воздушных судах
│   ├── aircraft.py              # Основная логика обработки
│   ├── opensky_client.py        # Клиент OpenSky Network API
│   └── polygon_processor.py     # Обработка полигонов регионов
│
├── parser/                      # Модуль парсинга данных
│   ├── parser_file.py           # Парсер Excel файлов с FTP
│   ├── region_stats_updater.py  # Обновление региональной статистики
│   └── downloads/               # Локальное хранилище файлов
│
├── grid/                        # Модуль генерации сеток
│   └── grid_generator.py        # Генератор квадратных и H3-гексагонов
│
├── area_bpla/                   # Модуль генерации площадок БПЛА
│   ├── generate_area_bpla.py    # Алгоритм размещения площадок
│   ├── run_generation.py        # Скрипт запуска
│   ├── test_module.py           # Тестирование модуля
│   ├── visualize.py             # Визуализация результатов
│   ├── integration_example.py   # Примеры интеграции
│   └── README.md                # Документация модуля
│
├── prediction/                  # Модуль прогнозирования
│   └── prediction.py            # Генерация прогнозов полетов
│
├── img_generator/               # Модуль генерации изображений
│   ├── fusionbrain_generator.py # FusionBrain API
│   └── gigachat_generator.py    # GigaChat API
│
├── openstreetmap/               # Модуль работы с OSM
│   └── openstreetmap.py         # Загрузка границ регионов
│
├── downloads/                   # Рабочие файлы
│   └── *.xlsx                   # Excel файлы с данными
│
├── log/                         # Логи системы
│   ├── log.log                  # Основной лог
│   └── hexagon_update.log       # Лог обновления гексагонов
│
├── main.py                      # Главная точка входа (фоновые процессы)
├── app.py                       # Flask API и веб-интерфейс
├── backup.py                    # Модуль резервного копирования
├── datalens.py                  # Интеграция с Yandex DataLens
├── settings.py                  # Конфигурация приложения
├── utils.py                     # Вспомогательные функции
├── requirements.txt             # Python-зависимости
└── README.md                    # Документация проекта
```

---

## 🔧 Модули системы

### 1. 📋 Parser Module (Парсинг данных)

**Файл:** `parser/parser_file.py`

**Функции:**
- Автоматическая загрузка файлов с FTP
- Парсинг Excel файлов с данными о полетах
- Извлечение координат и метаданных
- Геопривязка к регионам РФ
- Валидация и очистка данных

**Использование:**
```python
from parser.parser_file import FlightDataProcessor

processor = FlightDataProcessor()
processor.connect_to_db()
processor.process_all_files()  # Обработка всех файлов
```

**Основные таблицы:**
- `processed_files` — статус обработки файлов
- `processed_flights` — обработанные данные о полетах

---

### 2. ✈️ Aircraft Module (Сбор данных о судах)

**Файл:** `aircraft/aircraft.py`

**Функции:**
- Сбор данных с OpenSky Network API
- Фильтрация по территории России
- Геопривязка к регионам
- Обработка в реальном времени
- Автоматическая очистка устаревших данных

**Использование:**
```python
from aircraft.aircraft import Scheduler, DatabaseManager, AircraftDataProcessor
from aircraft.opensky_client import OpenSkyClient

db_manager = DatabaseManager(DB_CONFIG)
opensky_client = OpenSkyClient()
processor = AircraftDataProcessor(db_manager)
scheduler = Scheduler(db_manager, opensky_client, processor)

# Запуск сбора данных с интервалом 3600 секунд
scheduler.start_aircraft_data_thread(interval=3600)
```

**Особенности:**
- Многопоточная обработка
- Пул соединений MySQL
- R-Tree пространственный индекс для быстрой геопривязки
- Кеширование полигонов регионов

---

### 3. 🗺️ Grid Generator (Генератор сеток)

**Файл:** `grid/grid_generator.py`

**Функции:**
- Генерация квадратных сеток заданной площади
- Генерация гексагональных сеток H3 (разрешение 6)
- Расчет плотности полетов по ячейкам
- Обновление hexagon_id в processed_flights
- Фильтрация по территории России

**Использование:**
```python
from grid.grid_generator import GridGenerator

generator = GridGenerator(DB_CONFIG)
generator.connect()

# Генерация сеток для территории России
russia_bbox = (41.0, 19.0, 82.0, 180.0)  # (lat_min, lon_min, lat_max, lon_max)
generator.generate_grids(russia_bbox)

# Обновление привязки полетов к гексагонам
generator.update_processed_flights_hexagon_id_simple()
```

**Параметры:**
- Площадь ячейки: 1000 км² (по умолчанию, настраивается в таблице `settings`)
- H3 разрешение: 6 (средний размер ~36 км²)

---

### 4. 🏢 Area BPLA Generator (Генератор площадок)

**Файл:** `area_bpla/generate_area_bpla.py`

**Функции:**
- Анализ трафика полетов по гексагонам
- Учет запретных зон
- Оптимальное размещение 290 площадок
- Расчет рейтинга локаций
- Минимальное расстояние между площадками: 50 км

**Алгоритм:**
1. Загрузка гексагонов с данными о полетах
2. Загрузка запретных зон из таблицы `points`
3. Расчет рейтинга для каждого кандидата:
   - Трафик в радиусе 100 км (взвешенный по расстоянию)
   - Штраф за нахождение в запретной зоне: -10,000
   - Штраф за близость к другой площадке (<50 км): -5,000
4. Сортировка по рейтингу
5. Итеративный выбор лучших 290 площадок

**Использование:**
```python
from area_bpla.generate_area_bpla import AreaBPLAGenerator

generator = AreaBPLAGenerator(DB_CONFIG)
if generator.run():
    print("✅ Площадки успешно созданы")
```

**Результат:** Таблица `area_bpla` с оптимальными локациями

📖 **Подробная документация:** [area_bpla/README.md](area_bpla/README.md)

---

### 5. 📈 Prediction Module (Прогнозирование)

**Файл:** `prediction/prediction.py`

**Функции:**
- Анализ исторических данных
- Генерация прогнозов полетной активности
- Расчет трендов по регионам
- Предсказание на период до 2026 года

**Использование:**
```python
from prediction.prediction import FlightPredictorNew

predictor = FlightPredictorNew(DB_CONFIG)
predictor.generate_predictions(
    prediction_start='2025-08-01',
    prediction_end='2025-12-31'
)
```

---

### 6. 📊 Region Stats Updater (Статистика регионов)

**Файл:** `parser/region_stats_updater.py`

**Функции:**
- Расчет ежедневной статистики по регионам
- Агрегация месячных данных
- Анализ плотности полетов
- Расчет пиковых нагрузок

**Использование:**
```python
from parser.region_stats_updater import update_region_stats_main

update_region_stats_main()
```

---

### 7. 🤖 Image Generator (Генератор изображений)

**Файлы:**
- `img_generator/fusionbrain_generator.py`
- `img_generator/gigachat_generator.py`

**Функции:**
- Генерация изображений регионов через AI
- FusionBrain (Kandinsky)
- GigaChat альтернатива

---

### 8. 💾 Backup Module (Резервное копирование)

**Файл:** `backup.py`

**Функции:**
- Полное резервное копирование БД
- Автоматическое именование с timestamp
- Сжатие и архивация

**Использование:**
```python
from backup import BackupCreator

creator = BackupCreator(DB_CONFIG)
backup_name = creator.create_backup()
print(f"Бэкап создан: {backup_name}")
```

---

## 🌐 API и управление

### Web Dashboard

Запустите веб-интерфейс:

```bash
python app.py
```

Откройте браузер: **http://localhost:5000**

### REST API Endpoints

#### Обработка данных

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/update_region_stats` | Обновить статистику регионов |
| POST | `/process_files` | Обработать необработанные файлы |
| POST | `/update_aircraft_data` | Обновить данные о воздушных судах |
| POST | `/generate_grids` | Сгенерировать пространственные сетки |
| GET | `/reprocess/<filename>` | Повторно обработать файл |

#### Прогнозирование и аналитика

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/generate_predictions` | Генерация прогнозов полетов |
| GET | `/region_stats` | Статистика по регионам |

#### Утилиты

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/create_backup` | Создать резервную копию БД |
| GET | `/generate_datalens_token` | JWT токен для DataLens |
| POST | `/update_hexagon_ids` | Обновить hexagon_id в полетах |
| POST | `/process_polygons` | Обработать полигоны регионов |
| GET | `/background_status` | Статус фоновых процессов |

#### Примеры использования

**cURL:**
```bash
# Обновление статистики регионов
curl -X POST http://localhost:5000/update_region_stats

# Получение статистики
curl http://localhost:5000/region_stats

# Статус процессов
curl http://localhost:5000/background_status
```

**Python:**
```python
import requests

# Запуск обработки файлов
response = requests.post('http://localhost:5000/process_files')
print(response.json())

# Получение токена для DataLens
response = requests.get('http://localhost:5000/generate_datalens_token')
token = response.json()['token']
```

---

## 🗄️ База данных

### Основные таблицы

#### 1. `regions` — Регионы России
```sql
- id (INT) — ID региона
- name (VARCHAR) — Название региона
- polygon (GEOMETRY) — Полигон границы
- center_lat (DECIMAL) — Широта центра
- center_lon (DECIMAL) — Долгота центра
```

#### 2. `processed_flights` — Обработанные полеты
```sql
- id (INT) — Уникальный ID
- flight_date (DATE) — Дата полета
- start_time (TIME) — Время начала
- end_time (TIME) — Время окончания
- duration_minutes (INT) — Длительность (мин)
- start_lat (DECIMAL) — Широта старта
- start_lon (DECIMAL) — Долгота старта
- region_id (INT) — ID региона
- hexagon_id (INT) — ID гексагона H3
- filename (VARCHAR) — Исходный файл
```

#### 3. `aircraft` — Воздушные суда (реального времени)
```sql
- id (INT) — ID
- icao24 (VARCHAR) — ICAO24 код
- callsign (VARCHAR) — Позывной
- latitude (DECIMAL) — Широта
- longitude (DECIMAL) — Долгота
- altitude (FLOAT) — Высота (м)
- velocity (FLOAT) — Скорость (м/с)
- region_id (INT) — ID региона
- last_updated (DATETIME) — Время обновления
```

#### 4. `grid_hexagon` — Гексагональная сетка H3
```sql
- id (INT) — ID
- hexagon_index (VARCHAR) — H3 индекс
- center_lat (DECIMAL) — Широта центра
- center_lon (DECIMAL) — Долгота центра
- total_flights (INT) — Кол-во полетов
- region_id (INT) — ID региона
```

#### 5. `grid_square` — Квадратная сетка
```sql
- id (INT) — ID
- min_lat (DECIMAL) — Минимальная широта
- max_lat (DECIMAL) — Максимальная широта
- min_lon (DECIMAL) — Минимальная долгота
- max_lon (DECIMAL) — Максимальная долгота
- center_lat (DECIMAL) — Широта центра
- center_lon (DECIMAL) — Долгота центра
- total_flights (INT) — Кол-во полетов
```

#### 6. `area_bpla` — Площадки для БПЛА
```sql
- id (INT) — ID площадки
- center_lat (DECIMAL) — Широта
- center_lon (DECIMAL) — Долгота
- total_flights (INT) — Трафик
- hexagon_id (INT) — ID гексагона
- rating (FLOAT) — Рейтинг
- region_id (INT) — ID региона
- created_at (TIMESTAMP) — Дата создания
```

#### 7. `region_stats` — Статистика регионов
```sql
- id (INT) — ID
- region (VARCHAR) — Название региона
- date (DATE) — Дата
- total_flights (INT) — Всего полетов
- flight_density (FLOAT) — Плотность
- peak_load (INT) — Пиковая нагрузка
```

#### 8. `predictions` — Прогнозы
```sql
- id (INT) — ID
- region_id (INT) — ID региона
- prediction_date (DATE) — Дата прогноза
- predicted_flights (INT) — Прогноз полетов
- confidence (FLOAT) — Уверенность
```

#### 9. `processed_files` — Статус обработки файлов
```sql
- id (INT) — ID
- filename (VARCHAR) — Имя файла
- status (ENUM) — 'pending', 'processing', 'processed', 'error'
- procent (DECIMAL) — Процент обработки
- error_message (TEXT) — Сообщение об ошибке
- created_at (TIMESTAMP) — Дата создания
```

#### 10. `settings` — Настройки системы
```sql
- id (INT) — ID
- key_name (VARCHAR) — Ключ настройки
- value (VARCHAR) — Значение
- description (TEXT) — Описание
```

### Индексы и оптимизация

```sql
-- Пространственные индексы
CREATE SPATIAL INDEX idx_region_polygon ON regions(polygon);

-- Индексы для быстрого поиска
CREATE INDEX idx_flight_date ON processed_flights(flight_date);
CREATE INDEX idx_region_id ON processed_flights(region_id);
CREATE INDEX idx_hexagon_id ON processed_flights(hexagon_id);
CREATE INDEX idx_hexagon_index ON grid_hexagon(hexagon_index);
CREATE INDEX idx_aircraft_icao ON aircraft(icao24);
CREATE INDEX idx_aircraft_updated ON aircraft(last_updated);
```

---

## ⚙️ Конфигурация

### Файл settings.py

```python
# База данных
DB_CONFIG = {
    'user': 'username',
    'password': 'password', 
    'host': 'localhost',
    'port': '3306',
    'database': 'aerometr',
    'raise_on_warnings': True,
    'connect_timeout': 30000,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# FusionBrain AI
FUSION_BRAIN = {
    'api_key': 'your_api_key',
    'secret_key': 'your_secret_key'
}

# GigaChat
GIGACHAT_CREDENTIALS = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret'
}

# FTP
FTP_CONFIG = {
    'host': 'ftp.example.com',
    'username': 'username',
    'password': 'password',
    'remote_dir': '/path/to/files/',
}

# RSA ключ для JWT (DataLens)
private_key = b"""-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----"""
```

### Настройки в БД (таблица settings)

```sql
-- Площадь ячейки сетки
INSERT INTO settings (key_name, value, description)
VALUES ('grid_cell_area', '1000', 'Площадь ячейки сетки в км²');

-- Количество площадок БПЛА
INSERT INTO settings (key_name, value, description)
VALUES ('count_area_bpla', '290', 'Целевое количество площадок для БПЛА');
```

---

## 📚 Использование

### Основной процесс (main.py)

Запуск в фоновом режиме с автоматической обработкой:

```bash
python main.py
```

**Что происходит:**
1. Каждые **2 секунды** проверяется наличие необработанных файлов
2. При обнаружении запускается обработка
3. После обработки обновляется статистика регионов
4. Генерируются/обновляются пространственные сетки
5. Каждые **3600 секунд** обновляются данные о воздушных судах

### Web-интерфейс (app.py)

Запуск веб-сервера с панелью управления:

```bash
python app.py
```

Откройте `http://localhost:5000` для доступа к панели управления.

### Модули по отдельности

#### Парсинг файлов
```python
from parser.parser_file import FlightDataProcessor

processor = FlightDataProcessor()
processor.connect_to_db()
processor.process_all_files()
```

#### Сбор данных о судах
```python
from aircraft.aircraft import main

main()  # Запуск бесконечного цикла сбора данных
```

#### Генерация сеток
```python
from grid.grid_generator import GridGenerator

generator = GridGenerator(DB_CONFIG)
generator.connect()
russia_bbox = (41.0, 19.0, 82.0, 180.0)
generator.generate_grids(russia_bbox)
```

#### Генерация площадок БПЛА
```bash
cd area_bpla
python run_generation.py
```

или

```python
from area_bpla.generate_area_bpla import AreaBPLAGenerator

generator = AreaBPLAGenerator(DB_CONFIG)
generator.run()
```

#### Прогнозирование
```python
from prediction.prediction import FlightPredictorNew

predictor = FlightPredictorNew(DB_CONFIG)
predictor.generate_predictions(
    prediction_start='2025-08-01',
    prediction_end='2025-12-31'
)
```

#### Обновление статистики
```python
from parser.region_stats_updater import update_region_stats_main

update_region_stats_main()
```

#### Резервное копирование
```python
from backup import BackupCreator

creator = BackupCreator(DB_CONFIG)
backup_file = creator.create_backup()
print(f"✅ Бэкап создан: {backup_file}")
```

---

## 🚀 Производительность

| Метрика | Значение |
|---------|----------|
| **Обработка данных** | 50,000 записей/мин |
| **Нагрузка API** | 100 RPS |
| **Обновление aircraft** | Каждые 3600 сек |
| **Проверка файлов** | Каждые 2 сек |
| **Хранение данных** | Полная история |
| **Автоочистка** | Aircraft старше 24 часов |
| **Пул соединений** | 10 соединений MySQL |

### Оптимизация

- **R-Tree индекс** для быстрой геопривязки
- **Многопоточная обработка** в aircraft module
- **Кеширование полигонов** регионов
- **Batch операции** для массовых вставок
- **Prepared statements** для защиты от SQL-injection
- **Пространственные индексы** MySQL

---

## 👨‍💻 Разработка

### Структура кода

- **Модульность** — каждый модуль независим
- **Логирование** — все операции логируются
- **Обработка ошибок** — try-except блоки
- **Типизация** — type hints где возможно
- **Документация** — docstrings для всех функций

### Логирование

Логи сохраняются в:
- `log.log` — основной лог системы
- `log/hexagon_update.log` — лог обновления гексагонов

Формат:
```
2025-10-19 12:00:00 - INFO - Сообщение
2025-10-19 12:00:01 - ERROR - Ошибка
```

### Тестирование

```bash
# Тестирование модуля area_bpla
cd area_bpla
python test_module.py

# Проверка подключения к БД
python -c "from settings import DB_CONFIG; import mysql.connector; conn = mysql.connector.connect(**DB_CONFIG); print('✅ Подключение успешно')"
```

### Добавление нового модуля

1. Создайте папку модуля в корне проекта
2. Добавьте `__init__.py`
3. Реализуйте основную логику
4. Подключите в `main.py` или `app.py`
5. Обновите `requirements.txt` если нужны зависимости
6. Создайте документацию README.md в папке модуля

---

## 🤝 Вклад в проект

### Workflow

1. **Fork** репозитория
2. Создайте ветку: `git checkout -b feature/amazing-feature`
3. Внесите изменения и commit: `git commit -m 'Add amazing feature'`
4. Push в ветку: `git push origin feature/amazing-feature`
5. Откройте **Pull Request**

### Code Style

- PEP 8 для Python
- Docstrings для всех функций
- Type hints где возможно
- Комментарии на русском языке

---

## 📞 Поддержка

По вопросам использования и развития системы обращайтесь к команде разработки **Finance**.

- 🌐 **Сайт:** [https://aerometr.ru](https://aerometr.ru)
- 📧 **Email:** support@aerometr.ru
- 💬 **Telegram:** @aerometr_support

---

## 📄 Лицензия

Проприетарное программное обеспечение. Все права защищены © 2025 Команда Finance.

---

## 📊 Статистика проекта

- **Строк кода:** 10,000+
- **Модулей:** 8
- **Таблиц БД:** 10+
- **API Endpoints:** 15+
- **Обрабатываемых регионов:** 85

---

<div align="center">

**АЭРОМЕТР** — автоматизация аналитики полетов БПЛА для будущего российской авиации! ✈️

Made with ❤️ by Team Finance

</div>
