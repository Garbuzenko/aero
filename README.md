# ✈️ АЭРОМЕТР

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)

## 🌐 Ссылки

- **🌍 Демо-сайт**: [https://aerometr.ru](https://aerometr.ru)
- **📊 Презентация**: [Google Slides](https://docs.google.com/presentation/d/1tS-MUPT5ISglaNvYg3ztEVZ49lHhbtIfs-_1oyVkrAg/edit?usp=sharing)
- **🏗️ Архитектура**: [Диаграммы Archi/DRAW.IO](https://aerometr.ru/files/docs/drawio.html)

## 🎯 О проекте

**АЭРОМЕТР** — автоматизированная облачная система для сбора, обработки и анализа данных о полетах БПЛА в регионах России. Система интегрирует данные из множества источников и предоставляет комплексную аналитику полетной активности.

### Основные возможности

- 📊 **Анализ полетов БПЛА** по регионам РФ
- 🗺️ **Геопривязка** к официальным границам субъектов
- ⏱️ **Расчет длительности** и интенсивности полетов
- 📈 **Расширенная статистика** и визуализация
- 🤖 **AI-генерация** изображений регионов
- 🔄 **Реальное время** обработки данных

## 🏗️ Технологический стек

### Backend
- **Python** — основная логика обработки данных
- **PHP** — дополнительные модули
- **PostgreSQL** — основная база данных с PostGIS
- **MySQL** — вспомогательные данные

### Frontend
- Пользовательский интерфейс
- **HTML/CSS/JS** — базовая разметка и стили
- **Yandex Maps** — картографическая составляющая

### Внешние API
- **OpenSky Network** — данные о воздушных судах
- **SkyArc** — воздушная инфраструктура
- **FusionBrain AI** — генерация изображений
- **GigaChat** — альтернативная генерация
- **Overpass API** — границы регионов

## 📦 Быстрый старт

### Предварительные требования

- Python 3.8+
- PostgreSQL 12+ с PostGIS
- Node.js 14+
- MySQL 5.7+

### Установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/your-username/aerometr.git
cd aerometr
Настройка окружения

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
Установка зависимостей

bash
pip install -r requirements.txt
Настройка базы данных

sql
CREATE DATABASE aerometr;
CREATE EXTENSION postgis;
\i database/schema.sql
Конфигурация
Создайте settings.py на основе settings.example.py:

python
DB_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'aerometr',
    'port': '5432'
}
Запуск системы

bash
python main.py
🗃️ Структура проекта
text
aerometr/
├── aircraft/                 # Модуль обработки данных о воздушных судах
│   ├── aircraft.py          # Основной процессор данных
│   ├── opensky_client.py    # Клиент OpenSky API
│   └── polygon_processor.py # Обработка полигонов
├── parser/                  # Парсинг данных о полетах
│   ├── parser_file.py       # Парсер Excel файлов
│   └── region_stats_updater.py # Обновление статистики
├── grid/                    # Генерация пространственных сеток
│   └── grid_generator.py    # Генератор квадратных и гексагональных сеток
├── img_generator/           # Генерация изображений AI
│   ├── fusionbrain_generator.py
│   └── gigachat_generator.py
├── openstreetmap/           # Работа с OSM данными
│   └── openstreetmap.py
├── utils/                   # Вспомогательные утилиты
│   └── settings.py          # Настройки приложения
├── main.py                  # Точка входа приложения
├── backup.py                # Резервное копирование БД
└── datalens.py              # Интеграция с Yandex Datalens
🎮 Использование
Обработка данных о полетах
python
from parser.parser_file import FlightDataProcessor

# Автоматическая обработка всех файлов с FTP
processor = FlightDataProcessor()
processor.process_all_files()
Сбор данных о воздушных судах
python
from aircraft.aircraft import main

# Запуск сбора данных в реальном времени
main()
Генерация пространственных сеток
python
from grid.grid_generator import GridGenerator

generator = GridGenerator(DB_CONFIG)
generator.generate_grids(bbox=(41.0, 19.0, 82.0, 180.0))
📊 Модули системы
FlightDataProcessor
Парсинг Excel файлов с FTP

Извлечение координат и метаданных

Геопривязка к регионам РФ

Валидация и очистка данных

AircraftDataProcessor
Сбор данных с OpenSky Network

Обработка в реальном времени

Обновление статуса активных полетов

RegionStatsUpdater
Расчет ежедневной статистики

Агрегация месячных данных

Анализ плотности полетов

GridGenerator
Создание квадратных сеток

Генерация H3 гексагонов

Расчет плотности полетов

🔧 Конфигурация
Основные настройки в settings.py
python
# Настройки базы данных
DB_CONFIG = {
    'user': 'username',
    'password': 'password', 
    'host': 'localhost',
    'database': 'aerometr'
}

# Настройки FTP
FTP_CONFIG = {
    'host': 'ftp.example.com',
    'username': 'user',
    'password': 'pass',
    'remote_dir': '/files/'
}

# API ключи
FUSION_BRAIN = {
    'api_key': 'your_api_key',
    'secret_key': 'your_secret_key'
}
🗃️ База данных
Основные таблицы:

regions — регионы России с полигонами границ

processed_flights — обработанные данные о полетах

aircraft — данные о воздушных судах в реальном времени

region_stats — ежедневная статистика по регионам

grid_square/grid_hexagon — пространственные сетки

🚀 Производительность
⚡ Обработка: 50,000 записей в минуту

🔄 Нагрузка: 100 RPS

💾 Хранение: Полная история данных

🛡️ Надежность: Автоматическое восстановление

👥 Разработчики
Команда Finance

🤝 Вклад в проект
Форкните репозиторий

Создайте ветку для функции (git checkout -b feature/amazing-feature)

Закоммитьте изменения (git commit -m 'Add amazing feature')

Запушьте в ветку (git push origin feature/amazing-feature)

Откройте Pull Request

📞 Поддержка
По вопросам использования и развития системы обращайтесь к команде разработки.

АЭРОМЕТР — автоматизация аналитики полетов БПЛА для будущего российской авиации! ✈️

