# ✈️ АЭРОМЕТР

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![PHP](https://img.shields.io/badge/PHP-7.4+-purple.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

**Автоматизированная облачная система для сбора, обработки и анализа данных о полетах БПЛА в регионах России**

[🌐 Демо-сайт](https://aerometr.ru) • [📊 Презентация](https://docs.google.com/presentation/d/1tS-MUPT5ISglaNvYg3ztEVZ49lHhbtIfs-_1oyVkrAg/edit?usp=sharing) • [🏗️ Архитектура](https://aerometr.ru/files/docs/drawio.html) • [🎥 Видео](https://rutube.ru/video/private/6b444e00317e7986e054958e791480f2/?p=_AFpffCVQgO6-BAo_ONkRA)

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
  - [Backend](#-backend)
  - [Frontend](#-frontend)
  - [DataBase](#-database)
  - [DataLens](#-datalens)
- [API и управление](#-api-и-управление)
- [База данных](#-база-данных)
- [Производительность](#-производительность)
- [Команда](#-команда)

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
- Оптимальное **размещение 290 площадок** для БПЛА

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
│                      ПРЕДСТАВЛЕНИЕ                              │
├──────────────┬──────────────────────────┬─────────────────────┤
│  Flask API   │   PHP Web Frontend       │  DataLens Dashboards │
│  (Backend)   │   (Пользовательский UI)  │  (Визуализация)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Технологический стек

### Backend

| Технология | Назначение |
|-----------|-----------|
| **Python 3.8+** | Основная логика обработки данных |
| **Flask** | REST API и веб-интерфейс управления |
| **PHP 7.4+** | Веб-интерфейс пользователя |
| **MySQL 8.0+** | Реляционная база данных |
| **Shapely** | Обработка геометрических объектов |
| **H3** | Гексагональная геопространственная индексация |
| **Pandas** | Обработка табличных данных |
| **NumPy** | Численные вычисления |

### Frontend

| Технология | Описание |
|-----------|----------|
| **HTML/CSS/JS** | Базовая разметка и стили |
| **Yandex Maps API** | Картографическая составляющая |
| **jQuery** | JavaScript библиотека |
| **TCPDF** | Генерация PDF отчетов |
| **HTML2Canvas** | Экспорт карт в изображения |

### Внешние сервисы

| API | Описание |
|-----|----------|
| **OpenSky Network** | Данные о воздушных судах в реальном времени |
| **Overpass API (OSM)** | Геоданные и границы регионов |
| **SkyArc** | Запретные зоны и воздушная инфраструктура |
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
- PHP 7.4+ (для Frontend)
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
cd Backend
pip install -r requirements.txt
```

#### 4. Настройка базы данных

```sql
CREATE DATABASE aerometr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Импортируйте схему базы данных:
```bash
mysql -u username -p aerometr < DataBase/u3253297_hack.sql
```

#### 5. Конфигурация

Создайте файл `Backend/settings.py`:

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

**Backend (фоновый режим):**
```bash
cd Backend
python main.py
```

**Backend API (веб-интерфейс управления):**
```bash
cd Backend
python app.py
```

Откройте браузер: `http://localhost:5000`

**Frontend (пользовательский интерфейс):**
- Настройте веб-сервер (Apache/Nginx) для папки `Frontend/aerometr`
- Настройте подключение к БД в `Frontend/aerometr/config.php`

## 📁 Структура проекта

```
aerometr/
│
├── Backend/                         # Backend Python приложение
│   ├── aircraft/                    # Модуль сбора данных о воздушных судах
│   │   ├── aircraft.py              # Основная логика обработки
│   │   ├── opensky_client.py        # Клиент OpenSky Network API
│   │   ├── polygon_processor.py     # Обработка полигонов регионов
│   │   └── README.md                # Документация модуля
│   │
│   ├── parser/                      # Модуль парсинга данных
│   │   ├── parser_file.py           # Парсер Excel файлов с FTP
│   │   ├── region_stats_updater.py  # Обновление региональной статистики
│   │   ├── downloads/               # Локальное хранилище файлов
│   │   └── README.md                # Документация модуля
│   │
│   ├── grid/                        # Модуль генерации сеток
│   │   ├── grid_generator.py        # Генератор квадратных и H3-гексагонов
│   │   └── README.md                # Документация модуля
│   │
│   ├── area_bpla/                   # Модуль генерации площадок БПЛА
│   │   ├── generate_area_bpla.py    # Алгоритм размещения 290 площадок
│   │   └── README.md                # Документация модуля
│   │
│   ├── prediction/                  # Модуль прогнозирования
│   │   └── prediction.py            # Генерация прогнозов полетов
│   │
│   ├── img_generator/               # Модуль генерации изображений
│   │   ├── fusionbrain_generator.py # FusionBrain AI
│   │   └── gigachat_generator.py    # GigaChat API
│   │
│   ├── openstreetmap/               # Модуль работы с OSM
│   │   ├── openstreetmap.py         # Загрузка границ регионов
│   │   └── README.md                # Документация модуля
│   │
│   ├── log/                         # Логи системы
│   │   ├── log.log                  # Основной лог
│   │   └── hexagon_update.log       # Лог обновления гексагонов
│   │
│   ├── main.py                      # Главная точка входа (фоновые процессы)
│   ├── app.py                       # Flask API и веб-интерфейс управления
│   ├── backup.py                    # Модуль резервного копирования
│   ├── datalens.py                  # Интеграция с Yandex DataLens
│   ├── settings.py                  # Конфигурация приложения
│   ├── utils.py                     # Вспомогательные функции
│   ├── requirements.txt             # Python-зависимости
│   └── README.md                    # Документация Backend
│
├── Frontend/                        # Frontend PHP приложение
│   └── aerometr/                    # Веб-интерфейс пользователя
│       ├── index.php                # Главная страница
│       ├── config.php               # Конфигурация
│       ├── modules/                 # Модули интерфейса
│       │   ├── main/                # Главная страница с картой
│       │   ├── regions/             # Региональная аналитика
│       │   ├── gis/                 # ГИС-инструменты
│       │   ├── reports/             # Отчеты и статистика
│       │   └── settings/            # Настройки
│       ├── api/                     # API для фронтенда
│       ├── css/                     # Стили
│       ├── js/                      # JavaScript
│       └── img/                     # Изображения и медиа
│
├── DataBase/                        # База данных
│   ├── u3253297_hack.sql            # Полный дамп MySQL
│   └── README.md                    # Документация БД
│
├── Datalens/                        # Интеграция с Yandex DataLens
│   ├── lct.json                     # Конфигурация дашбордов
│   └── README.md                    # Документация интеграции
│
└── README.md                        # Главная документация проекта (этот файл)
```

---

## 🔧 Модули системы

### 📦 Backend

Детальная документация по каждому модулю Backend доступна в соответствующих README.md файлах:

#### 1. 📋 Parser Module — Парсинг данных о полетах

**Файлы:** `Backend/parser/` • [Документация](Backend/parser/README.md)

**Функции:**
- Автоматическая загрузка файлов с FTP
- Парсинг Excel файлов с данными о полетах
- Извлечение координат и метаданных
- Геопривязка к регионам РФ
- Валидация и очистка данных
- Генерация ежедневной и месячной статистики

**Использование:**
```python
from parser.parser_file import FlightDataProcessor

processor = FlightDataProcessor()
processor.connect_to_db()
processor.process_all_files()  # Обработка всех файлов
```

#### 2. ✈️ Aircraft Module — Сбор данных о судах

**Файлы:** `Backend/aircraft/` • [Документация](Backend/aircraft/README.md)

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

#### 3. 🗺️ Grid Generator — Генератор сеток

**Файлы:** `Backend/grid/` • [Документация](Backend/grid/README.md)

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

#### 4. 🏢 Area BPLA Generator — Генератор площадок

**Файлы:** `Backend/area_bpla/` • [Документация](Backend/area_bpla/README.md)

**Функции:**
- Анализ трафика полетов по гексагонам
- Учет запретных зон
- Оптимальное размещение 290 площадок
- Расчет рейтинга локаций
- Минимальное расстояние между площадками: 50 км
- Распределение по годам ввода в эксплуатацию (2026-2030)

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

#### 5. 📈 Prediction Module — Прогнозирование

**Файлы:** `Backend/prediction/`

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

#### 6. 🌍 OpenStreetMap Module — Загрузка границ

**Файлы:** `Backend/openstreetmap/` • [Документация](Backend/openstreetmap/README.md)

**Функции:**
- Загрузка административных границ России из OSM
- Поддержка нескольких уровней административного деления
- Конвертация в GeoJSON и специализированные форматы
- Расчет площади регионов в км²
- Определение центроидов для каждого региона

**Использование:**
```python
from openstreetmap.openstreetmap import fetch_osm_data, process_and_save_to_db

# Загрузка субъектов Федерации
raw_data = fetch_osm_data("6")
if raw_data:
    geojson_data = osm2geojson.json2geojson(raw_data)
    process_and_save_to_db(geojson_data, "6")
```

#### 7. 🤖 Image Generator — Генератор изображений

**Файлы:** `Backend/img_generator/`

**Функции:**
- Генерация изображений регионов через AI
- FusionBrain (Kandinsky)
- GigaChat альтернатива

#### 8. 💾 Backup Module — Резервное копирование

**Файл:** `Backend/backup.py`

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

### 🌐 Frontend

**Расположение:** `Frontend/aerometr/`

PHP-приложение с модульной архитектурой для пользовательского интерфейса.

#### Основные модули:

- **main/** — Главная страница с интерактивной картой
- **regions/** — Региональная аналитика и статистика
- **gis/** — ГИС-инструменты и визуализация
- **reports/** — Генерация отчетов и экспорт данных
- **settings/** — Настройки пользователя и системы

#### Возможности:

- Интерактивная карта на базе **Yandex Maps**
- Визуализация полетов БПЛА в реальном времени
- Статистика по регионам
- Генерация PDF отчетов (TCPDF)
- Экспорт данных в различных форматах
- Адаптивный дизайн

---

### 🗄️ DataBase

**Расположение:** `DataBase/` • [Документация](DataBase/README.md)

#### Содержимое:
- `u3253297_hack.sql` — Полный дамп MySQL базы данных

#### Основные таблицы:
- `processed_flights` — Обработанные данные о полетах
- `aircraft` — Воздушные суда в реальном времени
- `regions` — Регионы России с границами
- `grid_hexagon` — Гексагональная сетка H3
- `grid_square` — Квадратная сетка
- `area_bpla` — Площадки для БПЛА
- `region_stats` — Ежедневная статистика
- `region_stats_month` — Месячная статистика
- `predictions` — Прогнозы полетов
- `processed_files` — Статус обработки файлов
- `settings` — Настройки системы

**Размер:** ~200+ MB  
**Кодировка:** utf8mb4  
**Таблиц:** 15+

---

### 📊 DataLens

**Расположение:** `Datalens/` • [Документация](Datalens/README.md)

Интеграция с **Yandex DataLens** для визуализации и аналитики.

#### Компоненты:

- `lct.json` — Конфигурация дашбордов и чартов
- `../Backend/datalens.py` — Генератор JWT токенов

#### Основные дашборды:

1. **Главный дашборд** — Общая статистика по России
2. **Региональная аналитика** — Детальная статистика по регионам
3. **Площадки БПЛА** — Карта 290 площадок с рейтингами
4. **Real-time мониторинг** — Активные самолеты в реальном времени

#### JWT-аутентификация:

```python
import time
import jwt
from settings import private_key

now = int(time.time())
payload = {
    'embedId': "8e0tatm9jpjit",
    'dlEmbedService': "YC_DATALENS_EMBEDDING_SERVICE_MARK",
    'iat': now,
    'exp': now + 3600,  # Токен действителен 1 час
    "params": {}
}

encoded_token = jwt.encode(payload, private_key, algorithm='PS256')
```

---

## 🌐 API и управление

### Web Dashboard

Запустите веб-интерфейс управления:

```bash
cd Backend
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
- dof_date (DATE) — Дата полета
- atd_time (TIME) — Время начала
- ata_time (TIME) — Время окончания
- duration_min (INT) — Длительность (мин)
- departure_coords (VARCHAR) — Координаты старта
- arrival_coords (VARCHAR) — Координаты финиша
- region_id (INT) — ID региона
- hexagon_id (INT) — ID гексагона H3
- filename (VARCHAR) — Исходный файл
```

#### 3. `aircraft` — Воздушные суда (real-time)
```sql
- id (INT) — ID
- icao24 (VARCHAR) — ICAO24 код
- callsign (VARCHAR) — Позывной
- latitude (DECIMAL) — Широта
- longitude (DECIMAL) — Долгота
- baro_altitude (FLOAT) — Высота (м)
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

#### 5. `area_bpla` — Площадки для БПЛА
```sql
- id (INT) — ID площадки
- center_lat (DECIMAL) — Широта
- center_lon (DECIMAL) — Долгота
- total_flights (INT) — Трафик
- hexagon_id (INT) — ID гексагона
- rating (FLOAT) — Рейтинг
- region_id (INT) — ID региона
- year (INT) — Год ввода (2026-2030)
- created_at (TIMESTAMP) — Дата создания
```

#### 6. `region_stats` — Статистика регионов
```sql
- region (VARCHAR) — Название региона
- region_id (INT) — ID региона
- date (DATE) — Дата
- total_flights (INT) — Всего полетов
- flight_density (FLOAT) — Плотность
- peak_load (INT) — Пиковая нагрузка
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

## 📊 Статистика проекта

- **Строк кода:** 10,000+
- **Модулей:** 8
- **Таблиц БД:** 15+
- **API Endpoints:** 15+
- **Обрабатываемых регионов:** 85
- **Целевых площадок БПЛА:** 290

---

## 👥 Команда

Команда **Finance**

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

<div align="center">

**АЭРОМЕТР** — автоматизация аналитики полетов БПЛА для будущего российской авиации! ✈️

Made with ❤️ by Team Finance

**Дата:** 19 октября 2025  
**Версия:** 2.0.0

</div>

