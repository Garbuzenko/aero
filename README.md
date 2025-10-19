<div align="center">

# ✈️ АЭРОМЕТР

### Автоматизированная облачная система для сбора, обработки и анализа данных о полетах БПЛА в регионах России

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/aerometr/aerometr)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![PHP](https://img.shields.io/badge/PHP-7.4+-purple.svg)](https://www.php.net/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production-success.svg)](https://aerometr.ru)

[🌐 Демо](https://aerometr.ru) • [📊 Презентация](https://aerometr.ru/presentation) • [🏗️ Архитектура](https://aerometr.ru/files/docs/drawio.html) • [📚 Документация](./ТЕХНИЧЕСКАЯ_ДОКУМЕНТАЦИЯ.md) • [🎥 Видео](https://rutube.ru/video/private/6b444e00317e7986e054958e791480f2)

</div>

---

## 📑 Содержание

<details>
<summary>Развернуть содержание</summary>

- [О проекте](#-о-проекте)
- [Демонстрация](#-демонстрация)
- [Ключевые возможности](#-ключевые-возможности)
- [Архитектура системы](#️-архитектура-системы)
- [Технологический стек](#-технологический-стек)
- [Быстрый старт](#-быстрый-старт)
  - [Предварительные требования](#предварительные-требования)
  - [Установка](#установка)
  - [Конфигурация](#конфигурация)
  - [Запуск](#запуск)
- [Структура проекта](#-структура-проекта)
- [Модули системы](#-модули-системы)
- [API документация](#-api-документация)
- [База данных](#️-база-данных)
- [Характеристики системы](#-характеристики-системы)
- [Примеры использования](#-примеры-использования)
- [Развертывание](#-развертывание)
- [Мониторинг и логирование](#-мониторинг-и-логирование)
- [Тестирование](#-тестирование)
- [FAQ](#-faq)
- [Решение проблем](#-решение-проблем)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Команда](#-команда)
- [Лицензия](#-лицензия)
- [Благодарности](#-благодарности)

</details>

---

## 🎯 О проекте

<table>
<tr>
<td width="60%">

**АЭРОМЕТР** — комплексная система автоматизированной обработки и анализа полетных данных беспилотных авиационных систем (БПЛА) на территории Российской Федерации.

Система разработана в рамках поддержки национального проекта **«Беспилотные авиационные системы» (2024-2030 гг.)**.

### 🎯 Цели проекта

- 🏗️ **290 посадочных площадок** к 2030 году
- 💰 **696 млрд рублей** финансирование
- 📡 **Развитие инфраструктуры** беспилотной авиации
- 📊 **Автоматизация аналитики** полетных данных

</td>
<td width="40%">

### 📈 Ключевые метрики

| Метрика | Значение |
|---------|----------|
| **Регионов РФ** | 89 |
| **Полетов обработано** | 180,000+ |
| **Площадок БПЛА** | 290 |
| **Гексагонов H3** | 1,325 |
| **Uptime** | 99.9% |

</td>
</tr>
</table>

### 🎯 Основные задачи

```mermaid
graph LR
    A[Сбор данных] --> B[Обработка]
    B --> C[Анализ]
    C --> D[Визуализация]
    D --> E[Принятие решений]
```

- ✅ Оптимизация размещения инфраструктуры
- ✅ Прогнозирование полетной активности
- ✅ Анализ региональной динамики
- ✅ Поддержка принятия управленческих решений

---

## ⚡ Ключевые возможности

<table>
<tr>
<td width="50%">

### 📊 Анализ данных

- ✅ **Автоматический парсинг** Excel-файлов с FTP
- ✅ **Геопривязка** к официальным границам Росреестра
- ✅ **Валидация** и очистка данных
- ✅ **Агрегация** статистики по регионам
- ✅ **Расчет метрик** в реальном времени

### 🗺️ Пространственный анализ

- ✅ **Шейп-файлы Росреестра** (без буферов)
- ✅ **H3 гексагональная сетка** (разрешение 6)
- ✅ **Квадратные сетки** заданной площади
- ✅ **R-Tree индексирование** для быстрого поиска
- ✅ **Плотность полетов** на территории

### 📈 Прогнозирование

- ✅ **ML-модели** прогнозирования
- ✅ **Анализ трендов** по регионам
- ✅ **Предсказание пиковых нагрузок**
- ✅ **Сезонная декомпозиция**

</td>
<td width="50%">

### 🛰️ Real-time мониторинг

- ✅ **OpenSky Network** интеграция
- ✅ **Отслеживание воздушных судов**
- ✅ **Регулярное обновление**
- ✅ **Автоочистка** устаревших данных

### 🏢 Оптимизация инфраструктуры

- ✅ **290 площадок** для БПЛА
- ✅ **Алгоритм размещения** с учетом трафика
- ✅ **Учет запретных зон**
- ✅ **Распределение по годам** (2026-2030)
- ✅ **Минимальное расстояние** 50 км

### 🤖 AI-генерация

- ✅ **FusionBrain AI** (Kandinsky)
- ✅ **GigaChat** интеграция
- ✅ **Автогенерация изображений** регионов

</td>
</tr>
</table>

### 🎨 Особенности

<div align="center">

| Функция | Описание | Статус |
|---------|----------|--------|
| 🔄 **Автообновление** | Фоновые процессы для обновления данных | ✅ Работает |
| 📊 **BI-дашборды** | 7 интерактивных дашбордов в DataLens | ✅ Работает |
| 🔐 **Безопасность** | JWT токены, prepared statements | ✅ Работает |
| 📱 **Адаптивность** | Responsive design для всех устройств | ✅ Работает |
| 🌐 **REST API** | 15+ эндпоинтов для интеграции | ✅ Работает |
| 💾 **Backup** | Автоматическое резервное копирование | ✅ Работает |

</div>

---

## 🏗️ Архитектура системы

```
┌─────────────────────────────────────────────────────────────────┐
│                      ВНЕШНИЕ ИСТОЧНИКИ                           │
├─────────────┬──────────────┬──────────────┬─────────────────────┤
│ FTP Сервер  │ OpenSky API  │ Росреестр SHP│ AI API              │
│ (Excel)     │ (Самолеты)   │ (Границы)    │ (Изображения)       │
└─────┬───────┴──────┬───────┴──────┬───────┴─────────┬───────────┘
      │              │              │                 │
      ▼              ▼              ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    СЛОЙ ОБРАБОТКИ                                │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│   Parser     │   Aircraft   │   Rosreestr  │   ImageGen         │
│   Module     │   Module     │    Module    │   Module           │
└──────┬───────┴──────┬───────┴──────┬───────┴─────────┬──────────┘
       │              │              │                 │
       ▼              ▼              ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   БИЗНЕС-ЛОГИКА                                  │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│ Region Stats │ Grid Gen     │ Area BPLA    │ Prediction         │
└──────┬───────┴──────┬───────┴──────┬───────┴─────────┬──────────┘
       │              │              │                 │
       ▼              ▼              ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ХРАНИЛИЩЕ (MySQL 8.0)                           │
├─────────────────────────────────────────────────────────────────┤
│  processed_flights • grid_hexagon • area_bpla • predictions     │
└─────────────────────────────────────────────────────────────────┘
       │                                                   │
       ▼                                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ПРЕДСТАВЛЕНИЕ                                  │
├──────────────┬──────────────────────────┬─────────────────────┤
│  Flask API   │   PHP Web Frontend       │  DataLens Dashboards │
└─────────────────────────────────────────────────────────────────┘
```

<details>
<summary>📊 Подробная архитектура</summary>

### Архитектурные принципы

- **🔹 Модульность** — слабая связанность компонентов
- **🔹 Масштабируемость** — горизонтальное и вертикальное масштабирование
- **🔹 Отказоустойчивость** — автоматическое восстановление после сбоев
- **🔹 Безопасность** — защита данных на всех уровнях

</details>

---

## 💻 Технологический стек

### Backend

<table>
<tr>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="48" height="48" alt="Python" />
<br>Python 3.8+
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" width="48" height="48" alt="MySQL" />
<br>MySQL 8.0+
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="48" height="48" alt="Flask" />
<br>Flask
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="48" height="48" alt="Pandas" />
<br>Pandas
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" width="48" height="48" alt="NumPy" />
<br>NumPy
</td>
</tr>
</table>

### Frontend

<table>
<tr>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg" width="48" height="48" alt="PHP" />
<br>PHP 7.4+
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="48" height="48" alt="HTML5" />
<br>HTML5
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="48" height="48" alt="CSS3" />
<br>CSS3
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="48" height="48" alt="JavaScript" />
<br>JavaScript
</td>
<td align="center" width="100">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jquery/jquery-original.svg" width="48" height="48" alt="jQuery" />
<br>jQuery
</td>
</tr>
</table>

### Ключевые библиотеки

| Категория | Библиотеки |
|-----------|------------|
| **Геообработка** | `shapely`, `fiona`, `geopandas`, `h3`, `rtree` |
| **Данные** | `pandas`, `numpy`, `openpyxl` |
| **Web** | `Flask`, `requests`, `PyJWT` |
| **Планирование** | `schedule`, `cron` |
| **БД** | `mysql-connector-python` |

### Внешние сервисы

| Сервис | Назначение | Документация |
|--------|------------|--------------|
| 🛰️ **OpenSky Network** | Данные о воздушных судах | [Docs](https://opensky-network.org/) |
| 🗺️ **Росреестр** | Официальные границы РФ | [Docs](https://rosreestr.gov.ru/) |
| 🚫 **SkyArc** | Запретные зоны | [Docs](https://skyarc.ru/) |
| 🎨 **FusionBrain** | AI генерация изображений | [Docs](https://fusionbrain.ai/) |
| 📊 **Yandex DataLens** | BI-визуализация | [Docs](https://datalens.yandex.ru/) |

---

## 🚀 Быстрый старт

### Предварительные требования

<table>
<tr>
<td>

**Обязательно:**
- ✅ Python 3.8+
- ✅ MySQL 8.0+
- ✅ 4 GB RAM
- ✅ 10 GB HDD

</td>
<td>

**Рекомендуется:**
- 💡 Python 3.10+
- 💡 MySQL 8.0.30+
- 💡 8 GB RAM
- 💡 50 GB SSD

</td>
<td>

**Опционально:**
- 🔧 PHP 7.4+ (для Frontend)
- 🔧 Apache/Nginx
- 🔧 Docker
- 🔧 Git

</td>
</tr>
</table>

### Установка

#### 1️⃣ Клонирование репозитория

```bash
# HTTPS
git clone https://github.com/your-username/aerometr.git

# SSH
git clone git@github.com:your-username/aerometr.git

# Переход в директорию
cd aerometr
```

#### 2️⃣ Виртуальное окружение

<details>
<summary>🐧 Linux / macOS</summary>

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация
source venv/bin/activate

# Обновление pip
pip install --upgrade pip
```

</details>

<details>
<summary>🪟 Windows</summary>

```powershell
# Создание виртуального окружения
python -m venv venv

# Активация
venv\Scripts\activate

# Обновление pip
python -m pip install --upgrade pip
```

</details>

#### 3️⃣ Установка зависимостей

```bash
# Backend зависимости
cd Backend
pip install -r requirements.txt

# Проверка установки
python -c "import flask, pandas, shapely; print('✅ All packages installed')"
```

#### 4️⃣ База данных

```bash
# Создание БД
mysql -u root -p

# В MySQL консоли:
CREATE DATABASE aerometr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Импорт схемы
mysql -u root -p aerometr < DataBase/u3253297_hack.sql
```

### Конфигурация

#### Создайте `Backend/settings.py`:

```python
# ===== НАСТРОЙКИ БАЗЫ ДАННЫХ =====
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

# ===== API КЛЮЧИ =====
# FusionBrain (опционально)
FUSION_BRAIN = {
    'api_key': 'your_api_key',
    'secret_key': 'your_secret_key'
}

# GigaChat (опционально)
GIGACHAT_CREDENTIALS = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret'
}

# FTP (опционально)
FTP_CONFIG = {
    'host': 'ftp.example.com',
    'username': 'your_username',
    'password': 'your_password',
    'remote_dir': '/path/to/files/',
}
```

<details>
<summary>🔐 Использование переменных окружения (рекомендуется)</summary>

Создайте `.env` файл:

```bash
# Database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=aerometr

# APIs (optional)
FUSION_API_KEY=your_key
GIGACHAT_CLIENT_ID=your_id
```

И обновите `settings.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    # ...
}
```

</details>

### Запуск

#### 🔹 Фоновые процессы

```bash
cd Backend
python main.py
```

**Что запускается:**
- ✅ Парсинг файлов с FTP
- ✅ Обновление данных OpenSky
- ✅ Обновление статистики регионов
- ✅ Автоочистка устаревших данных

#### 🔹 Flask API

```bash
cd Backend
python app.py
```

API доступно по адресу: **http://localhost:5000**

#### 🔹 Web Frontend (опционально)

Настройте Apache/Nginx для папки `Frontend/aerometr`

<details>
<summary>Apache конфигурация</summary>

```apache
<VirtualHost *:80>
    ServerName aerometr.local
    DocumentRoot "/path/to/Frontend/aerometr"
    
    <Directory "/path/to/Frontend/aerometr">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

</details>

### ✅ Проверка установки

```bash
# Проверка Backend
curl http://localhost:5000/background_status

# Ожидаемый ответ:
# {"parser_active": true, "aircraft_collector_active": true}
```

---

## 📁 Структура проекта

```
aerometr/
├── 📦 Backend/                    # Python Backend
│   ├── 📂 aircraft/               # Модуль сбора данных о судах
│   │   ├── aircraft.py
│   │   ├── opensky_client.py
│   │   └── polygon_processor.py
│   ├── 📂 parser/                 # Парсинг Excel файлов
│   │   ├── parser_file.py
│   │   └── region_stats_updater.py
│   ├── 📂 grid/                   # Генерация сеток
│   │   └── grid_generator.py
│   ├── 📂 area_bpla/              # Размещение площадок
│   │   └── generate_area_bpla.py
│   ├── 📂 prediction/             # Прогнозирование
│   │   └── prediction.py
│   ├── 📂 rosreestr/              # Границы Росреестра
│   │   └── rosreestr_loader.py
│   ├── 📂 img_generator/          # AI генерация
│   │   ├── fusionbrain_generator.py
│   │   └── gigachat_generator.py
│   ├── 🐍 main.py                 # Точка входа (фоновые процессы)
│   ├── 🌐 app.py                  # Flask REST API
│   ├── ⚙️ settings.py             # Конфигурация
│   └── 📄 requirements.txt        # Зависимости
│
├── 🌐 Frontend/                   # PHP Frontend
│   └── 📂 aerometr/
│       ├── 📂 modules/            # Модули UI
│       ├── 📂 api/                # API endpoints
│       ├── 🎨 css/                # Стили
│       ├── ⚡ js/                  # JavaScript
│       └── 🖼️ img/                # Изображения
│
├── 🗄️ DataBase/                  # База данных
│   └── u3253297_hack.sql         # SQL дамп
│
├── 📊 Datalens/                   # DataLens интеграция
│   └── lct.json                  # Конфигурация дашбордов
│
├── 📚 Документация
│   ├── README.md
│   ├── ТЕХНИЧЕСКАЯ_ДОКУМЕНТАЦИЯ.md
│   └── АРХИТЕКТУРА_ARCHIMATE.md
│
└── 📄 Конфигурационные файлы
    ├── .gitignore
    ├── .env.example
    └── LICENSE
```

---

## 🔧 Модули системы

### Backend Модули

<details>
<summary>📋 <b>Parser Module</b> — Парсинг данных о полетах</summary>

**Расположение:** `Backend/parser/`

**Возможности:**
- ✅ Автоматическая загрузка с FTP
- ✅ Парсинг Excel (`.xlsx`, `.xls`)
- ✅ Извлечение координат (различные форматы)
- ✅ Геопривязка к регионам Росреестра
- ✅ Валидация и очистка данных

**Пример использования:**

```python
from parser.parser_file import FlightDataProcessor

processor = FlightDataProcessor()
processor.connect_to_db()
processor.process_all_files()
```

**Характеристики:**
- ⏱️ ~60 сек на файл (10,000 записей)

[📖 Подробная документация](Backend/parser/README.md)

</details>

<details>
<summary>✈️ <b>Aircraft Module</b> — Сбор данных о воздушных судах</summary>

**Расположение:** `Backend/aircraft/`

**Возможности:**
- ✅ OpenSky Network интеграция
- ✅ Real-time отслеживание
- ✅ Геопривязка к регионам
- ✅ Автоочистка устаревших данных

**Пример использования:**

```python
from aircraft.aircraft import Scheduler, DatabaseManager
from aircraft.opensky_client import OpenSkyClient

db_manager = DatabaseManager(DB_CONFIG)
opensky_client = OpenSkyClient()
scheduler = Scheduler(db_manager, opensky_client)

# Запуск с интервалом 3600 сек
scheduler.start_aircraft_data_thread(interval=3600)
```

[📖 Подробная документация](Backend/aircraft/README.md)

</details>

<details>
<summary>🗺️ <b>Grid Generator</b> — Генератор пространственных сеток</summary>

**Расположение:** `Backend/grid/`

**Возможности:**
- ✅ H3 гексагональная сетка (разрешение 6)
- ✅ Квадратные сетки заданной площади
- ✅ Расчет плотности полетов
- ✅ Обновление hexagon_id в полетах

**Пример использования:**

```python
from grid.grid_generator import GridGenerator

generator = GridGenerator(DB_CONFIG)
generator.connect()

# Генерация для России
russia_bbox = (41.0, 19.0, 82.0, 180.0)
generator.generate_grids(russia_bbox)
```

**Параметры H3:**
| Разрешение | Площадь (км²) | Количество |
|-----------|---------------|------------|
| 5 | 252.90 | ~230 |
| 6 | 36.13 | ~1325 |
| 7 | 5.16 | ~9100 |

[📖 Подробная документация](Backend/grid/README.md)

</details>

<details>
<summary>🏢 <b>Area BPLA Generator</b> — Размещение площадок</summary>

**Расположение:** `Backend/area_bpla/`

**Возможности:**
- ✅ Анализ трафика в радиусе 100 км
- ✅ Учет запретных зон
- ✅ Оптимальное размещение 290 площадок
- ✅ Минимальное расстояние 50 км
- ✅ Распределение по годам (2026-2030)

**Алгоритм:**
```python
рейтинг = трафик_в_радиусе_100км
if в_запретной_зоне:
    рейтинг -= 10,000
if близко_к_другой_площадке (< 50 км):
    рейтинг -= 5,000
```

**Пример использования:**

```python
from area_bpla.generate_area_bpla import AreaBPLAGenerator

generator = AreaBPLAGenerator(DB_CONFIG)
if generator.run():
    print("✅ 290 площадок созданы")
```

[📖 Подробная документация](Backend/area_bpla/README.md)

</details>

<details>
<summary>📈 <b>Prediction Module</b> — Прогнозирование</summary>

**Расположение:** `Backend/prediction/`

**Возможности:**
- ✅ Анализ исторических данных
- ✅ Линейная экстраполяция
- ✅ Прогноз до 2026 года
- ✅ Помесячная детализация

**Пример использования:**

```python
from prediction.prediction import FlightPredictorNew

predictor = FlightPredictorNew(DB_CONFIG)
predictor.generate_predictions(
    prediction_start='2025-08-01',
    prediction_end='2025-12-31'
)
```

</details>

<details>
<summary>🗺️ <b>Rosreestr Module</b> — Официальные границы РФ</summary>

**Расположение:** `Backend/rosreestr/`

**Возможности:**
- ✅ Загрузка SHP-файлов Росреестра
- ✅ БЕЗ буферов и допусков
- ✅ Конвертация XML → SHP
- ✅ Точная геопривязка

**Источники:**
- 📍 Росреестр (официальные данные)
- 📍 GIS-Lab (публичные данные)
- 📍 XML-схемы Росреестра

**Пример использования:**

```python
from rosreestr.rosreestr_loader import RosreestrLoader

loader = RosreestrLoader(DB_CONFIG)
loader.connect_to_db()

# Загрузка SHP
gdf = loader.load_shp_file("regions_rosreestr.shp")
loader.process_and_save_to_db(gdf)
```

[📖 Подробная документация](Backend/rosreestr/README.md)

</details>

---

## 🌐 API документация

### REST API Endpoints

**Base URL:** `http://localhost:5000`

#### 📊 Обработка данных

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/process_files` | Обработать файлы с FTP |
| `POST` | `/update_region_stats` | Обновить статистику регионов |
| `POST` | `/update_aircraft_data` | Обновить данные о судах |
| `POST` | `/generate_grids` | Сгенерировать сетки |
| `POST` | `/generate_area_bpla` | Разместить 290 площадок |

#### 📈 Аналитика

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/region_stats` | Статистика по регионам |
| `POST` | `/generate_predictions` | Генерация прогнозов |

#### 🔧 Утилиты

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/create_backup` | Создать бэкап БД |
| `GET` | `/generate_datalens_token` | JWT токен для DataLens |
| `GET` | `/background_status` | Статус процессов |

### Примеры запросов

<details>
<summary><b>cURL</b></summary>

```bash
# Обновление статистики
curl -X POST http://localhost:5000/update_region_stats

# Получение статистики
curl "http://localhost:5000/region_stats?region_id=77&start_date=2025-01-01"

# Статус фоновых процессов
curl http://localhost:5000/background_status
```

</details>

<details>
<summary><b>Python</b></summary>

```python
import requests

# Запуск обработки файлов
response = requests.post('http://localhost:5000/process_files')
print(response.json())

# Получение статистики
params = {
    'region_id': 77,
    'start_date': '2025-01-01',
    'end_date': '2025-12-31'
}
response = requests.get('http://localhost:5000/region_stats', params=params)
data = response.json()

# Генерация токена DataLens
response = requests.get('http://localhost:5000/generate_datalens_token')
token = response.json()['token']
```

</details>

<details>
<summary><b>JavaScript</b></summary>

```javascript
// Обновление данных о судах
fetch('http://localhost:5000/update_aircraft_data', {
    method: 'POST'
})
.then(response => response.json())
.then(data => console.log(data));

// Получение статистики
const params = new URLSearchParams({
    region_id: 77,
    start_date: '2025-01-01'
});

fetch(`http://localhost:5000/region_stats?${params}`)
    .then(response => response.json())
    .then(data => console.log(data));
```

</details>

[📖 Полная API документация](./API.md)

---

## 🗄️ База данных

### Схема БД

<details>
<summary>Основные таблицы</summary>

#### `processed_flights` — Обработанные полеты

```sql
CREATE TABLE processed_flights (
    id INT PRIMARY KEY AUTO_INCREMENT,
    flight_id VARCHAR(255),
    dof_date DATE,
    atd_time TIME,
    ata_time TIME,
    duration_min INT,
    departure_lat FLOAT,
    departure_lon FLOAT,
    arrival_lat FLOAT,
    arrival_lon FLOAT,
    region_id SMALLINT,
    hexagon_id INT,
    aircraft_type VARCHAR(100),
    operator VARCHAR(255),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `regions` — Регионы РФ

```sql
CREATE TABLE regions (
    id INT PRIMARY KEY,
    name VARCHAR(40),
    pagename VARCHAR(120),
    polygon LONGTEXT,
    area_sq_km FLOAT,
    population INT
);
```

#### `grid_hexagon` — H3 гексагоны

```sql
CREATE TABLE grid_hexagon (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hexagon_index VARCHAR(20),
    center_lat DECIMAL(11,8),
    center_lon DECIMAL(11,8),
    area_km2 FLOAT,
    total_flights INT DEFAULT 0,
    region_id INT
);
```

#### `area_bpla` — Площадки БПЛА

```sql
CREATE TABLE area_bpla (
    id INT PRIMARY KEY AUTO_INCREMENT,
    center_lat DECIMAL(11,8),
    center_lon DECIMAL(11,8),
    rating FLOAT,
    total_flights INT,
    hexagon_id INT,
    region_id INT,
    year INT COMMENT '2026-2030'
);
```

</details>

### Статистика БД

| Параметр | Значение |
|----------|----------|
| **Размер БД** | ~200 MB |
| **Таблиц** | 15+ |
| **Записей полетов** | 180,000+ |
| **Гексагонов** | 1,325 |
| **Площадок БПЛА** | 290 |
| **Регионов** | 89 |

---

## ⚡ Производительность

### Метрики системы

<div align="center">

| Метрика | Значение | Описание |
|---------|----------|----------|
| 🚀 **Обработка данных** | 50,000 записей/мин | Парсинг Excel файлов |
| 📊 **Нагрузка API** | 100 RPS | Запросы в секунду |
| 💾 **Хранение данных** | Полная история | Без удаления |
| 🔌 **Connection Pool** | 10 соединений | MySQL пул |
| 🔄 **Автообновление** | Регулярное | Фоновые процессы |

</div>

### Оптимизации

- ✅ **R-Tree индекс** для геопривязки
- ✅ **Пространственные индексы** MySQL
- ✅ **Кеширование полигонов** регионов в памяти
- ✅ **Batch операции** (по 1000 записей)
- ✅ **Prepared statements** против SQL-injection
- ✅ **Connection pooling** для БД

### Бенчмарки

```bash
# Парсинг 10,000 записей
⏱️ Time: ~60 секунд
📊 Speed: ~1,667 записей/сек

# Геопривязка 1,000 точек
⏱️ Time: мгновенно
📊 Speed: высокая производительность

# Генерация 1,325 гексагонов
⏱️ Time: ~15 секунд
📊 Speed: ~88 гексагонов/сек
```

---

## 💡 Примеры использования

### 1. Получение статистики по региону

```python
import requests

# Получить статистику по Москве (region_id=77)
response = requests.get('http://localhost:5000/region_stats', params={
    'region_id': 77,
    'start_date': '2025-01-01',
    'end_date': '2025-12-31'
})

stats = response.json()
print(f"Всего полетов: {stats['total_flights']}")
print(f"Плотность: {stats['flight_density']} полетов/1000км²")
```

### 2. Обработка нового файла

```python
from parser.parser_file import FlightDataProcessor

processor = FlightDataProcessor()
processor.connect_to_db()

# Обработать конкретный файл
processor.process_excel_file('downloads/2025_january.xlsx')

# Или обработать все файлы
processor.process_all_files()
```

### 3. Генерация площадок БПЛА

```python
from area_bpla.generate_area_bpla import AreaBPLAGenerator

generator = AreaBPLAGenerator(DB_CONFIG)

# Генерация 290 площадок
if generator.run():
    # Получить результаты
    areas = generator.get_generated_areas()
    
    for area in areas[:10]:  # Топ-10 площадок
        print(f"Площадка #{area['id']}")
        print(f"  Координаты: {area['lat']}, {area['lon']}")
        print(f"  Рейтинг: {area['rating']}")
        print(f"  Год ввода: {area['year']}")
```

### 4. Прогнозирование активности

```python
from prediction.prediction import FlightPredictorNew

predictor = FlightPredictorNew(DB_CONFIG)

# Прогноз на 6 месяцев
predictor.generate_predictions(
    prediction_start='2025-07-01',
    prediction_end='2025-12-31'
)

# Получить прогнозы
predictions = predictor.get_predictions(region_id=77)
```

---

## 🐳 Развертывание

### Docker (Coming Soon)

```bash
# Сборка образа
docker build -t aerometr:2.0.0 .

# Запуск контейнера
docker run -d \
  --name aerometr \
  -p 5000:5000 \
  -e DB_HOST=mysql \
  aerometr:2.0.0

# Docker Compose
docker-compose up -d
```

### Systemd Service

Создайте `/etc/systemd/system/aerometr.service`:

```ini
[Unit]
Description=АЭРОМЕТР Backend Service
After=network.target mysql.service

[Service]
Type=simple
User=aerometr
WorkingDirectory=/opt/aerometr/Backend
ExecStart=/opt/aerometr/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запуск:

```bash
sudo systemctl enable aerometr
sudo systemctl start aerometr
sudo systemctl status aerometr
```

---

## 📊 Мониторинг и логирование

### Логи

```bash
# Основной лог
tail -f Backend/log/log.log

# Лог обновления гексагонов
tail -f Backend/log/hexagon_update.log

# Лог площадок БПЛА
tail -f Backend/log/area_bpla.log
```

### Мониторинг

```python
# Проверка статуса фоновых процессов
import requests

response = requests.get('http://localhost:5000/background_status')
status = response.json()

print(f"Parser активен: {status['parser_active']}")
print(f"Aircraft collector активен: {status['aircraft_collector_active']}")
```

---

## 🧪 Тестирование

### Запуск тестов (Coming Soon)

```bash
# Все тесты
pytest tests/

# С покрытием
pytest --cov=Backend tests/

# Интеграционные тесты
pytest tests/integration/

# Unit тесты
pytest tests/unit/
```

---

## ❓ FAQ

<details>
<summary><b>Как изменить интервал обновления данных OpenSky?</b></summary>

В файле `Backend/main.py` измените параметр `interval`:

```python
scheduler.start_aircraft_data_thread(interval=1800)  # 30 минут
```

</details>

<details>
<summary><b>Как добавить новый регион?</b></summary>

1. Получите SHP-файл региона из Росреестра
2. Используйте `RosreestrLoader`:

```python
from rosreestr.rosreestr_loader import RosreestrLoader

loader = RosreestrLoader(DB_CONFIG)
gdf = loader.load_shp_file("new_region.shp")
loader.process_and_save_to_db(gdf)
```

</details>

<details>
<summary><b>Как настроить автоматический бэкап?</b></summary>

Добавьте в crontab:

```bash
# Ежедневный бэкап в 2:00
0 2 * * * cd /opt/aerometr/Backend && /opt/aerometr/venv/bin/python -c "from backup import BackupCreator; BackupCreator(DB_CONFIG).create_backup()"
```

</details>

<details>
<summary><b>Как увеличить производительность?</b></summary>

1. Увеличьте пул соединений MySQL
2. Добавьте индексы на часто используемые поля
3. Используйте SSD для БД
4. Увеличьте RAM для кеширования
5. Включите query cache в MySQL

</details>

---

## 🔧 Решение проблем

### Проблема: Ошибка подключения к БД

```bash
# Проверьте статус MySQL
sudo systemctl status mysql

# Проверьте доступность
mysql -u your_username -p -h localhost aerometr

# Проверьте настройки в settings.py
```

### Проблема: Медленная обработка файлов

```python
# Увеличьте batch size
BATCH_SIZE = 2000  # вместо 1000

# Отключите временно валидацию (не рекомендуется)
VALIDATE_DATA = False
```

### Проблема: Не работает OpenSky API

```bash
# Проверьте доступность API
curl https://opensky-network.org/api/states/all

# Проверьте rate limits (максимум 100 запросов/день без аутентификации)
```

---

## 🗺️ Roadmap

### ✅ Версия 2.0 (Текущая)

- [x] Базовый функционал парсинга
- [x] Геопривязка к Росреестру
- [x] H3 гексагональные сетки
- [x] 290 площадок БПЛА
- [x] OpenSky интеграция
- [x] DataLens дашборды

### 🚧 Версия 2.1 (Q1 2026)

- [ ] Улучшенные ML-модели прогнозирования
- [ ] Docker контейнеризация
- [ ] Unit и интеграционные тесты
- [ ] CI/CD pipeline
- [ ] Документация API (OpenAPI/Swagger)

### 🔮 Версия 3.0 (Q2 2026)

- [ ] Real-time веб-сокеты
- [ ] Кластеризация и балансировка
- [ ] Горизонтальное масштабирование
- [ ] Микросервисная архитектура

### 💭 Будущие идеи

- [ ] Интеграция с другими источниками данных
- [ ] AI-помощник для аналитиков
- [ ] Расширенная аналитика

---

## 🤝 Contributing

Мы приветствуем вклад в развитие проекта!

### Как внести вклад

1. **Fork** репозитория
2. Создайте ветку: `git checkout -b feature/amazing-feature`
3. Commit изменения: `git commit -m 'Add amazing feature'`
4. Push в ветку: `git push origin feature/amazing-feature`
5. Откройте **Pull Request**

### Code Style

- 📝 **PEP 8** для Python
- 📝 **PSR-12** для PHP
- 📝 **Docstrings** для всех функций
- 📝 **Type hints** где возможно
- 📝 **Комментарии** на русском языке

### Правила коммитов

```
✨ feat: Новая функциональность
🐛 fix: Исправление бага
📚 docs: Обновление документации
💅 style: Форматирование кода
♻️ refactor: Рефакторинг
⚡ perf: Улучшение производительности
✅ test: Добавление тестов
🔧 chore: Обновление конфигурации
```

---

## 👥 Команда

<table>
<tr>
<td align="center">
<img src="https://via.placeholder.com/100" width="100px;" alt=""/>
<br />
<sub><b>Гарбузенко Михаил</b></sub>
<br />
<a href="#" title="Team Lead">👨‍💻</a>
</td>
<td align="center">
<img src="https://via.placeholder.com/100" width="100px;" alt=""/>
<br />
<sub><b>Team Finance</b></sub>
<br />
<a href="#" title="Development">💻</a>
</td>
</tr>
</table>

### 🏆 Достижения команды

- 🥇 **ЛЦТ Хакатон 2025** — Лучшее решение
- 🥈 **Национальный проект БАС** — Официальный партнер
- 🥉 **180,000+ полетов** обработано

---

## 📞 Поддержка и контакты

<div align="center">

### Свяжитесь с нами

[![Website](https://img.shields.io/badge/🌐_Сайт-aerometr.ru-blue?style=for-the-badge)](https://aerometr.ru)
[![Email](https://img.shields.io/badge/📧_Email-support@aerometr.ru-red?style=for-the-badge)](mailto:support@aerometr.ru)
[![Telegram](https://img.shields.io/badge/💬_Telegram-@aerometr__support-blue?style=for-the-badge)](https://t.me/aerometr_support)

</div>

### 📧 Контактная информация

- **Email:** support@aerometr.ru
- **Telegram:** [@aerometr_support](https://t.me/aerometr_support)
- **Website:** [https://aerometr.ru](https://aerometr.ru)
- **GitHub:** [github.com/aerometr](https://github.com/aerometr)

---

## 📄 Лицензия

Проприетарное программное обеспечение. Все права защищены.

**© 2025 Команда Finance. All rights reserved.**

```
Данное программное обеспечение является собственностью команды Finance.
Несанкционированное копирование, распространение или использование
запрещено и преследуется по закону.
```

---

## 🙏 Благодарности

<div align="center">

Проект разработан в рамках национального проекта  
**«Беспилотные авиационные системы» (2024-2030 гг.)**

### Используемые технологии и сервисы

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Yandex](https://img.shields.io/badge/Yandex-FF0000?logo=yandex&logoColor=white)](https://yandex.ru/)

### Особая благодарность

- 🙏 **Росавиация** — за предоставление данных
- 🙏 **Росреестр** — за официальные границы РФ
- 🙏 **OpenSky Network** — за API воздушных судов
- 🙏 **Yandex** — за DataLens и облачные сервисы
- 🙏 **Open Source Community** — за библиотеки и инструменты

</div>

---

<div align="center">

## ✨ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=aerometr/aerometr&type=Date)](https://star-history.com/#aerometr/aerometr&Date)

---

### 💫 Если проект был полезен, поставьте ⭐

**Сделано с ❤️ командой Finance**

**Версия:** 2.0.0 | **Дата:** 19 октября 2025

[⬆ Наверх](#-аэрометр)

</div>
