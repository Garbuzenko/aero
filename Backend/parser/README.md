# 📊 Parser Module — Модуль парсинга данных о полетах

## 📖 Описание

Модуль **Parser** предназначен для автоматического сбора, обработки и анализа данных о полетах БПЛА из Excel-файлов. Обеспечивает полный цикл обработки: от загрузки файлов с FTP до геопривязки полетов и генерации расширенной статистики по регионам.

## 🎯 Назначение

Модуль решает следующие задачи:

- ✅ **Автоматическая загрузка** файлов с FTP-сервера
- ✅ **Парсинг Excel-файлов** с данными о полетах
- ✅ **Извлечение метаданных** (оператор, тип, координаты, высота, длительность)
- ✅ **Геопривязка полетов** к регионам РФ
- ✅ **Валидация и очистка** данных
- ✅ **Генерация статистики** по регионам (ежедневная и месячная)
- ✅ **Предотвращение дубликатов** через UNIQ_STR

---

## 📁 Структура модуля

```
parser/
├── parser_file.py           # Основной парсер Excel файлов
├── region_stats_updater.py  # Генератор статистики регионов
├── downloads/               # Локальное хранилище Excel файлов
└── README.md               # Документация модуля (этот файл)
```

---

## 🔧 Компоненты модуля

### 1. 📄 parser_file.py — FlightDataProcessor

**Основной класс для обработки данных о полетах**

#### Функциональность

- **Загрузка с FTP**
  - Автоматическое подключение к FTP
  - Скачивание .xlsx файлов
  - Отслеживание обработанных файлов в БД

- **Парсинг Excel файлов**
  - Поддержка множественных листов
  - Автоматическое определение структуры листа
  - Обработка 15+ типов полей данных

- **Извлечение данных**
  ```
  • DOF (Date of Flight) — дата полета
  • DEP/ARR — точки вылета/прилета с координатами
  • SHR (Supplementary Hazard Report) — дополнительные данные
  • OPR (Operator) — оператор полета
  • STS (Status) — особые статусы (FFR, SAR, STATE)
  • ATD/ATA (Actual Time Departure/Arrival) — время вылета/прилета
  • EET (Estimated Elapsed Time) — расчетное время полета
  • RMK (Remarks) — замечания
  • Координаты точек маршрута
  • Высота полета
  • Количество БПЛА
  ```

- **Геопривязка**
  - Использование Shapely STRtree для быстрого поиска
  - Определение региона по координатам вылета/прилета
  - Кеширование полигонов регионов

- **Расчет производных данных**
  - Длительность полета (duration_min)
  - Расстояние между точками
  - Классификация времени суток (morning/afternoon/evening/night)

#### Использование

```python
from parser.parser_file import FlightDataProcessor

# Инициализация процессора
processor = FlightDataProcessor()

# Подключение к БД
if processor.connect_to_db():
    # Обработка всех необработанных файлов
    processor.process_all_files()
    
    # Или обработка конкретного файла
    processor.process_file_from_db("2025.xlsx")
```

#### Основные методы

| Метод | Описание |
|-------|----------|
| `connect_to_db()` | Подключение к базе данных |
| `download_files_from_ftp()` | Загрузка файлов с FTP |
| `process_all_files()` | Обработка всех необработанных файлов |
| `process_file_from_db(filename)` | Обработка конкретного файла |
| `extract_operator(text)` | Извлечение оператора из текста |
| `extract_sts(text)` | Извлечение статуса (FFR/SAR/STATE) |
| `parse_coordinates(text)` | Парсинг координат |
| `calculate_flight_duration()` | Расчет длительности полета |

#### Формат данных в Excel

Модуль автоматически определяет структуру листа по заголовкам:

**Вариант 1: Отдельные столбцы**
```
DOF | DEP | ARR | SHR | ATD | ATA | EET | RMK | ...
```

**Вариант 2: Объединенное поле АДРЕСА**
```
DOF | АДРЕСА (DEP/ARR/SHR) | ATD | ATA | ...
```

#### Обработка особых случаев

- **Многострочные блоки**: OPR/, RMK/, STS/
- **Телефонные номера**: автоматическое удаление
- **Множественные пробелы**: нормализация
- **Переносы строк**: очистка и объединение

---

### 2. 📈 region_stats_updater.py — RegionStatsUpdaterFixed

**Генератор расширенной статистики по регионам**

#### Функциональность

- **Ежедневная статистика** (`region_stats`)
  - Общее количество полетов
  - Распределение по времени суток
  - Пиковая нагрузка (максимум полетов в час)
  - Средняя длительность полета
  - Плотность полетов на 1000 км²
  - Количество последовательных дней без полетов

- **Месячная статистика** (`region_stats_month`)
  - Агрегация данных по месяцам
  - Медиана ежедневных полетов
  - Процентное изменение относительно прошлого месяца
  - Процентное распределение по времени суток

- **Поддержка типов данных**
  - `download` — реальные данные
  - `prediction` — прогнозные данные

#### Использование

```python
from parser.region_stats_updater import update_region_stats_main

# Запуск обновления статистики
success = update_region_stats_main()
```

**Или через класс:**

```python
from parser.region_stats_updater import RegionStatsUpdaterFixed
from settings import DB_CONFIG

updater = RegionStatsUpdaterFixed(DB_CONFIG)
updater.update_region_stats()
```

#### Настройка периода обработки

Даты настраиваются через таблицу `settings`:

```sql
-- Период реальных данных
INSERT INTO settings (key_name, value, description)
VALUES ('start_date', '2024-01-01', 'Начальная дата обработки');

INSERT INTO settings (key_name, value, description)
VALUES ('end_date', '2025-07-31', 'Конечная дата обработки');

-- Период прогнозных данных
INSERT INTO settings (key_name, value, description)
VALUES ('start_date_prediction', '2025-08-01', 'Начало прогнозного периода');

INSERT INTO settings (key_name, value, description)
VALUES ('end_date_prediction', '2025-12-31', 'Конец прогнозного периода');
```

#### Основные методы

| Метод | Описание |
|-------|----------|
| `create_region_stats_table()` | Создание таблицы ежедневной статистики |
| `create_region_stats_month_table()` | Создание таблицы месячной статистики |
| `get_flights_data(start, end)` | Получение данных о полетах |
| `calculate_stats()` | Расчет статистики |
| `populate_region_stats()` | Заполнение ежедневной статистики |
| `populate_region_stats_month()` | Заполнение месячной статистики |

---

## 🗄️ База данных

### Таблица `processed_files`

Отслеживание статуса обработки файлов:

```sql
CREATE TABLE processed_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) UNIQUE NOT NULL,
    status ENUM('pending', 'processing', 'processed', 'error') DEFAULT 'pending',
    procent DECIMAL(5,2) DEFAULT 0.00,
    error_message TEXT,
    processed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Таблица `processed_flights`

Основная таблица обработанных данных:

```sql
CREATE TABLE processed_flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dof_date DATE NOT NULL,
    atd_time TIME,
    ata_time TIME,
    duration_min INT,
    
    -- Геоданные
    departure_coords VARCHAR(100),
    arrival_coords VARCHAR(100),
    departure_region VARCHAR(100),
    arrival_region VARCHAR(100),
    region_id INT,
    hexagon_id INT,
    
    start_lat DECIMAL(10,7),
    start_lon DECIMAL(10,7),
    end_lat DECIMAL(10,7),
    end_lon DECIMAL(10,7),
    
    -- Метаданные
    operator TEXT,
    aircraft_type_code VARCHAR(50),
    registration VARCHAR(50),
    sts VARCHAR(20),
    
    -- Характеристики полета
    altitude_max INT,
    quantity INT,
    eet_info VARCHAR(50),
    
    -- Служебные поля
    time_of_day ENUM('morning', 'afternoon', 'evening', 'night'),
    prediction ENUM('download', 'prediction') DEFAULT 'download',
    filename VARCHAR(255),
    uniq_str VARCHAR(255) UNIQUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_dof_date (dof_date),
    INDEX idx_region_id (region_id),
    INDEX idx_hexagon_id (hexagon_id),
    INDEX idx_prediction (prediction),
    INDEX idx_filename (filename)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Таблица `region_stats`

Ежедневная статистика по регионам:

```sql
CREATE TABLE region_stats (
    region VARCHAR(100) NOT NULL,
    region_id INT,
    date DATE NOT NULL,
    prediction ENUM('download','prediction') NOT NULL DEFAULT 'download',
    
    -- Основная статистика
    total_flights INT,
    peak_load INT,
    flight_density DOUBLE,
    zero_days INT,
    
    -- Распределение по времени суток
    morning_flights INT,
    afternoon_flights INT,
    evening_flights INT,
    night_flights INT,
    
    -- Характеристики полетов
    avg_duration_min INT,
    eet_info DOUBLE,
    quantity DOUBLE,
    altitude_info DOUBLE,
    
    -- Агрегаты за месяц
    avg_daily_flights DOUBLE,
    median_daily_flights DOUBLE,
    monthly_change DOUBLE,
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (region, date, prediction),
    INDEX idx_region_date (region, date),
    INDEX idx_date (date),
    INDEX idx_region_id (region_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Таблица `region_stats_month`

Месячная агрегированная статистика:

```sql
CREATE TABLE region_stats_month (
    region VARCHAR(100) NOT NULL,
    region_id INT,
    month VARCHAR(7) NOT NULL,  -- YYYY-MM
    prediction ENUM('download','prediction') NOT NULL DEFAULT 'download',
    
    -- Агрегаты за месяц
    total_flights INT,
    avg_flight_duration DOUBLE,
    peak_load INT,
    flight_density DOUBLE,
    monthly_change DOUBLE,
    
    -- Распределение по времени суток
    morning_flights INT,
    afternoon_flights INT,
    evening_flights INT,
    night_flights INT,
    
    -- Проценты времени суток
    morning_percent DOUBLE,
    afternoon_percent DOUBLE,
    evening_percent DOUBLE,
    night_percent DOUBLE,
    
    -- Медианные значения
    median_daily_flights DOUBLE,
    zero_days INT,
    
    -- Характеристики
    eet_info DOUBLE,
    quantity DOUBLE,
    altitude_info DOUBLE,
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (region, month, prediction),
    INDEX idx_region_month (region, month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## ⚙️ Конфигурация

### Настройки в settings.py

```python
# База данных
DB_CONFIG = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': '3306',
    'database': 'aerometr',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# FTP для загрузки файлов
FTP_CONFIG = {
    'host': 'ftp.example.com',
    'username': 'user',
    'password': 'password',
    'remote_dir': '/files/'
}
```

### Настройки уникальности (UNIQ_STR)

Поля для формирования уникального ключа:

```python
UNIQ_STR_COLUMNS = [
    'dof_date',
    'registration',
    'operator',
    'aircraft_type_code',
    'filename',
    'region_id',
    'prediction',
    'sts',
    'time_of_day',
    'departure_coords'
]
```

---

## 🚀 Использование

### Обработка файлов из FTP

```python
from parser.parser_file import FlightDataProcessor

processor = FlightDataProcessor()
processor.connect_to_db()

# Загрузка и обработка всех файлов
processor.download_files_from_ftp()
processor.process_all_files()
```

### Обработка конкретного файла

```python
processor = FlightDataProcessor()
processor.connect_to_db()

# Обработка одного файла
processor.process_file_from_db("2025_parse_file.xlsx")
```

### Обновление статистики регионов

```python
from parser.region_stats_updater import update_region_stats_main

# Полное обновление статистики
success = update_region_stats_main()
if success:
    print("✅ Статистика обновлена успешно")
```

### Интеграция в основной процесс

```python
# main.py
from parser.parser_file import FlightDataProcessor
from parser.region_stats_updater import update_region_stats_main

def process_data():
    # 1. Обработка файлов
    processor = FlightDataProcessor()
    processor.connect_to_db()
    processor.process_all_files()
    
    # 2. Обновление статистики
    update_region_stats_main()
    
    print("✅ Обработка завершена")

if __name__ == "__main__":
    process_data()
```

---

## 📊 Примеры данных

### Пример записи в processed_flights

```python
{
    'dof_date': '2025-10-19',
    'atd_time': '14:30:00',
    'ata_time': '15:45:00',
    'duration_min': 75,
    'departure_coords': '55.7558,37.6173',
    'arrival_coords': '59.9311,30.3609',
    'departure_region': 'Москва',
    'arrival_region': 'Санкт-Петербург',
    'region_id': 77,
    'operator': 'ООО "Аэро"',
    'aircraft_type_code': 'DJI-M300',
    'registration': 'RA-12345',
    'sts': 'STATE',
    'altitude_max': 120,
    'quantity': 1,
    'time_of_day': 'afternoon',
    'prediction': 'download',
    'filename': '2025.xlsx'
}
```

### Пример записи в region_stats

```python
{
    'region': 'Москва',
    'region_id': 77,
    'date': '2025-10-19',
    'prediction': 'download',
    'total_flights': 245,
    'peak_load': 35,
    'flight_density': 2.45,
    'morning_flights': 82,
    'afternoon_flights': 98,
    'evening_flights': 52,
    'night_flights': 13,
    'avg_duration_min': 68,
    'zero_days': 0
}
```

---

## 🔍 Анализ данных

### SQL-запросы для анализа

```sql
-- Топ-10 регионов по количеству полетов
SELECT region, SUM(total_flights) as total
FROM region_stats
WHERE prediction = 'download'
GROUP BY region
ORDER BY total DESC
LIMIT 10;

-- Динамика полетов по дням
SELECT date, SUM(total_flights) as daily_total
FROM region_stats
WHERE region = 'Москва'
  AND prediction = 'download'
ORDER BY date;

-- Распределение по времени суток
SELECT 
    region,
    SUM(morning_flights) as morning,
    SUM(afternoon_flights) as afternoon,
    SUM(evening_flights) as evening,
    SUM(night_flights) as night
FROM region_stats
WHERE prediction = 'download'
GROUP BY region
ORDER BY (morning + afternoon + evening + night) DESC
LIMIT 10;

-- Месячная статистика с изменениями
SELECT 
    region,
    month,
    total_flights,
    monthly_change,
    peak_load
FROM region_stats_month
WHERE prediction = 'download'
ORDER BY region, month;
```

---

## 🛠️ Troubleshooting

### Проблема: Файлы не загружаются с FTP

**Решение:**
1. Проверьте настройки FTP в `settings.py`
2. Проверьте подключение: `ftp ftp.example.com`
3. Проверьте права доступа к папке

### Проблема: Неверно определяются регионы

**Решение:**
1. Проверьте наличие полигонов в таблице `regions`
2. Убедитесь, что координаты корректны
3. Проверьте кеш полигонов: `processor.load_regions()`

### Проблема: Дублирование записей

**Решение:**
- Проверьте настройки `UNIQ_STR_COLUMNS`
- Убедитесь, что индекс `UNIQUE (uniq_str)` существует

### Проблема: Медленная обработка

**Решение:**
1. Увеличьте размер batch: `self.batch_size = 500`
2. Добавьте индексы в БД
3. Используйте batch-вставки

---

## 📈 Производительность

| Метрика | Значение |
|---------|----------|
| **Скорость парсинга** | 50,000 записей/мин |
| **Размер batch** | 200-500 записей |
| **Время обработки файла** | 2-10 минут (зависит от размера) |
| **Обновление статистики** | 30-120 секунд |
| **Использование памяти** | 200-500 МБ |

---

## 🔐 Безопасность

- **SQL Injection**: Использование prepared statements
- **Валидация данных**: Проверка типов и форматов
- **Обработка ошибок**: Try-except блоки
- **Логирование**: Все операции записываются в log

---

## 📝 Логирование

Логи сохраняются в `../log.log`:

```
2025-10-19 12:00:00 - INFO - Начало обработки файла: 2025.xlsx
2025-10-19 12:00:01 - INFO - Найдено листов: 3
2025-10-19 12:00:02 - INFO - Обработка листа: Sheet1
2025-10-19 12:00:10 - INFO - Обработано записей: 1500
2025-10-19 12:00:10 - INFO - ✅ Файл обработан успешно
```

---

## 🤝 Интеграция с другими модулями

### С Grid Generator

```python
# После обработки файлов обновляем сетки
from grid.grid_generator import GridGenerator

processor = FlightDataProcessor()
processor.process_all_files()

# Обновление гексагонов
generator = GridGenerator(DB_CONFIG)
generator.update_processed_flights_hexagon_id_simple()
```

### С Aircraft Module

```python
# Обработка данных из OpenSky и парсера
from aircraft.aircraft import Scheduler
from parser.parser_file import FlightDataProcessor

# Параллельная обработка
processor = FlightDataProcessor()
scheduler = Scheduler(db_manager, opensky_client, aircraft_processor)
```

---

## 👨‍💻 Разработка

### Добавление нового типа поля

1. Добавьте обработчик в `FlightDataProcessor`
2. Обновите схему БД
3. Добавьте в `UNIQ_STR_COLUMNS` при необходимости
4. Обновите тесты

### Добавление новой статистики

1. Добавьте поле в таблицу `region_stats`
2. Обновите метод `calculate_stats()`
3. Обновите batch-вставку
4. Добавьте в месячную агрегацию при необходимости

---

## 📄 Лицензия

Проприетарное программное обеспечение. Все права защищены © 2025 Команда Finance.

---

**Дата:** 19 октября 2025  
**Версия документации:** 1.0.0  
**Модуль:** Parser

