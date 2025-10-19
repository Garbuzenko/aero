# ✈️ Aircraft Module — Модуль сбора данных о воздушных судах

## 📖 Описание

Модуль **Aircraft** обеспечивает сбор и обработку данных о воздушных судах в **реальном времени** с использованием OpenSky Network API. Выполняет геопривязку самолетов к регионам России, обрабатывает запретные зоны и автоматически очищает устаревшие данные.

## 🎯 Назначение

Модуль решает следующие задачи:

- ✅ **Сбор данных в реальном времени** с OpenSky Network
- ✅ **Геопривязка судов** к регионам РФ
- ✅ **Фильтрация по территории** России (bbox)
- ✅ **Обработка запретных зон** и ограничений полетов
- ✅ **Автоматическая очистка** устаревших данных (старше 24 часов)
- ✅ **Многопоточная обработка** для высокой производительности
- ✅ **Пул соединений** MySQL для оптимизации запросов

---

## 📁 Структура модуля

```
aircraft/
├── aircraft.py            # Основная логика обработки данных
├── opensky_client.py      # Клиент OpenSky Network API
├── polygon_processor.py   # Обработка полигонов запретных зон
└── README.md             # Документация модуля (этот файл)
```

---

## 🔧 Компоненты модуля

### 1. ✈️ aircraft.py — Основная обработка

#### Классы

##### DatabaseManager

Управление соединениями с базой данных:

```python
class DatabaseManager:
    def __init__(self, config):
        self.connection_pool = None
        self.init_connection_pool(config)
    
    def get_connection(self):
        """Получение соединения из пула"""
        
    def safe_execute(self, cursor, query, params=None):
        """Безопасное выполнение запроса с повторами"""
        
    def safe_executemany(self, cursor, query, params):
        """Массовая вставка с обработкой ошибок"""
```

**Особенности:**
- Пул из 10 соединений
- Автоматический retry при потере соединения
- Graceful recovery после ошибок

##### AircraftDataProcessor

Обработка и сохранение данных о самолетах:

```python
class AircraftDataProcessor:
    def process_and_save(self, states_data):
        """Обработка данных из OpenSky и сохранение в БД"""
        
    def clear_old_data(self):
        """Удаление данных старше 24 часов"""
        
    def determine_region(self, lat, lon):
        """Определение региона по координатам"""
```

**Обрабатываемые данные:**
- ICAO24 код
- Позывной (callsign)
- Координаты (latitude, longitude)
- Высота (altitude)
- Скорость (velocity)
- Курс (heading)
- Вертикальная скорость (vertical_rate)

##### Scheduler

Планировщик фоновых задач:

```python
class Scheduler:
    def fetch_and_save_aircraft_data(self):
        """Получение и сохранение данных о самолетах"""
        
    def start_aircraft_data_thread(self, interval=600):
        """Запуск фонового потока с интервалом"""
```

**Параметры:**
- Интервал обновления: 600-3600 секунд (по умолчанию)
- Автоматическая очистка: каждые 24 часа
- Фоновый режим (daemon thread)

#### Функции

##### load_regions()

Загрузка полигонов регионов и построение пространственного индекса:

```python
def load_regions():
    """
    - Загружает полигоны регионов из БД
    - Строит R-Tree пространственный индекс
    - Кеширует данные для быстрого доступа
    """
```

**Оптимизация:**
- R-Tree индекс для O(log n) поиска
- Prepared geometries для ускорения проверок
- Thread-safe загрузка с блокировками

---

### 2. 🌐 opensky_client.py — OpenSky Network API

Клиент для работы с OpenSky Network:

```python
class OpenSkyClient:
    def __init__(self, username=None, password=None):
        self.base_url = "https://opensky-network.org/api"
        self.auth = (username, password) if username and password else None
        
    def get_all_aircrafts(self, bbox=None):
        """Получение всех самолетов в заданном bbox"""
        
    def test_connection(self):
        """Тестирование подключения к API"""
```

#### Использование

```python
from aircraft.opensky_client import OpenSkyClient

# Инициализация клиента (без аутентификации)
client = OpenSkyClient()

# Получение всех самолетов над Россией
russia_bbox = (19.0, 41.0, 180.0, 82.0)  # (lon_min, lat_min, lon_max, lat_max)
data = client.get_all_aircrafts(bbox=russia_bbox)

if data and 'states' in data:
    print(f"Найдено самолетов: {len(data['states'])}")
```

#### Формат данных OpenSky

```python
state_vector = [
    icao24,         # 0: ICAO24 код (строка)
    callsign,       # 1: Позывной (строка)
    origin_country, # 2: Страна регистрации (строка)
    time_position,  # 3: Unix timestamp позиции
    last_contact,   # 4: Unix timestamp последнего контакта
    longitude,      # 5: Долгота (float)
    latitude,       # 6: Широта (float)
    baro_altitude,  # 7: Барометрическая высота (м)
    on_ground,      # 8: На земле (bool)
    velocity,       # 9: Скорость (м/с)
    true_track,     # 10: Курс (градусы)
    vertical_rate,  # 11: Вертикальная скорость (м/с)
    sensors,        # 12: ID сенсоров
    geo_altitude,   # 13: Геометрическая высота (м)
    squawk,         # 14: Squawk код
    spi,            # 15: Special Position Identification
    position_source # 16: Источник позиции (0-3)
]
```

---

### 3. 🗺️ polygon_processor.py — Обработка полигонов

Работа с запретными зонами и ограничениями полетов:

```python
class PolygonProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def get_data(self, lat, lng):
        """Получение данных о зонах с SkyArc API"""
        
    def add_date_to_points(self, data):
        """Добавление данных о запретных зонах в БД"""
        
    def swap_coordinates(self, features):
        """Обмен координат (lat, lon) <-> (lon, lat)"""
        
    def calculate_intersections(self):
        """Расчет пересечений полигонов с регионами"""
```

#### Использование

```python
from aircraft.polygon_processor import PolygonProcessor

processor = PolygonProcessor(db_manager)

# Получение запретных зон для координаты
data = processor.get_data(55.7558, 37.6173)  # Москва

# Сохранение в БД
if data:
    processor.add_date_to_points(data)
    
# Расчет пересечений с регионами
processor.calculate_intersections()
```

#### Типы зон

Обрабатываются зоны из **SkyArc API**:
- Запретные зоны
- Ограниченные зоны
- Опасные зоны
- Временные ограничения

---

## 🗄️ База данных

### Таблица `aircraft`

Хранение данных о воздушных судах в реальном времени:

```sql
CREATE TABLE aircraft (
    id INT AUTO_INCREMENT PRIMARY KEY,
    icao24 VARCHAR(10) NOT NULL,
    callsign VARCHAR(50),
    origin_country VARCHAR(100),
    time_position INT,
    last_contact INT,
    longitude DECIMAL(10,7),
    latitude DECIMAL(10,7),
    baro_altitude FLOAT,
    on_ground BOOLEAN,
    velocity FLOAT,
    true_track FLOAT,
    vertical_rate FLOAT,
    geo_altitude FLOAT,
    squawk VARCHAR(10),
    
    -- Геопривязка
    region VARCHAR(100),
    region_id INT,
    
    -- Метаданные
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_icao24 (icao24),
    INDEX idx_callsign (callsign),
    INDEX idx_region_id (region_id),
    INDEX idx_last_updated (last_updated),
    INDEX idx_coordinates (latitude, longitude)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Таблица `points`

Хранение запретных зон и ограничений:

```sql
CREATE TABLE points (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    polygon JSON,
    
    -- Временные ограничения
    startDateTime DATETIME,
    endDateTime DATETIME,
    schedule TEXT,
    
    -- Высотные ограничения
    lowerLimit TEXT,
    upperLimit TEXT,
    lowerLimitValue INT,
    upperLimitValue INT,
    lowerLimitUnits VARCHAR(10),
    upperLimitUnits VARCHAR(10),
    lowerLimitVerticalReference VARCHAR(50),
    upperLimitVerticalReference VARCHAR(50),
    
    -- Метаданные
    nameSpace VARCHAR(100),
    uuid VARCHAR(100),
    airspaceType VARCHAR(50),
    meta TEXT,
    isActive BOOLEAN DEFAULT 1,
    
    INDEX idx_active (isActive),
    INDEX idx_airspace_type (airspaceType)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## ⚙️ Конфигурация

### Настройки в settings.py

```python
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
```

### Параметры модуля

```python
# Bbox России (для фильтрации OpenSky)
RUSSIA_BBOX = (19.0, 41.0, 180.0, 82.0)  # (lon_min, lat_min, lon_max, lat_max)

# Интервал обновления (секунды)
UPDATE_INTERVAL = 600  # 10 минут

# Время хранения данных (часы)
DATA_RETENTION_HOURS = 24

# Размер пула соединений
CONNECTION_POOL_SIZE = 10

# Максимальное количество retry
MAX_RETRIES = 3
```

---

## 🚀 Использование

### Запуск в фоновом режиме

```python
from aircraft.aircraft import Scheduler, DatabaseManager, AircraftDataProcessor
from aircraft.opensky_client import OpenSkyClient
from settings import DB_CONFIG

# Инициализация компонентов
db_manager = DatabaseManager(DB_CONFIG)
opensky_client = OpenSkyClient()
aircraft_processor = AircraftDataProcessor(db_manager)

# Создание планировщика
scheduler = Scheduler(db_manager, opensky_client, aircraft_processor)

# Запуск фонового потока (обновление каждые 3600 секунд)
thread = scheduler.start_aircraft_data_thread(interval=3600)

# Ждем завершения (или Ctrl+C)
try:
    thread.join()
except KeyboardInterrupt:
    print("Остановка...")
```

### Разовое обновление данных

```python
from aircraft.aircraft import Scheduler, DatabaseManager, AircraftDataProcessor
from aircraft.opensky_client import OpenSkyClient
from settings import DB_CONFIG

db_manager = DatabaseManager(DB_CONFIG)
opensky_client = OpenSkyClient()
aircraft_processor = AircraftDataProcessor(db_manager)

scheduler = Scheduler(db_manager, opensky_client, aircraft_processor)

# Однократное получение данных
scheduler.fetch_and_save_aircraft_data()
```

### Обработка запретных зон

```python
from aircraft.polygon_processor import PolygonProcessor
from aircraft.aircraft import DatabaseManager
from settings import DB_CONFIG

db_manager = DatabaseManager(DB_CONFIG)
processor = PolygonProcessor(db_manager)

# Установка полигонов для всех точек
processor.set_points_polygon()

# Расчет пересечений с регионами
processor.calculate_intersections()
```

---

## 📊 Примеры данных

### Пример записи в aircraft

```python
{
    'icao24': 'a12345',
    'callsign': 'AFL123',
    'origin_country': 'Russian Federation',
    'time_position': 1697712345,
    'last_contact': 1697712348,
    'longitude': 37.6173,
    'latitude': 55.7558,
    'baro_altitude': 10668.0,
    'on_ground': False,
    'velocity': 250.5,
    'true_track': 90.0,
    'vertical_rate': 0.0,
    'geo_altitude': 10700.0,
    'squawk': '2000',
    'region': 'Москва',
    'region_id': 77,
    'last_updated': '2025-10-19 12:30:45'
}
```

---

## 🔍 Анализ данных

### SQL-запросы для мониторинга

```sql
-- Количество активных самолетов по регионам
SELECT region, COUNT(*) as aircraft_count
FROM aircraft
WHERE last_updated >= NOW() - INTERVAL 1 HOUR
GROUP BY region
ORDER BY aircraft_count DESC;

-- Самолеты на большой высоте
SELECT icao24, callsign, baro_altitude, region
FROM aircraft
WHERE baro_altitude > 10000
  AND last_updated >= NOW() - INTERVAL 30 MINUTE
ORDER BY baro_altitude DESC;

-- Средняя скорость по регионам
SELECT region, 
       COUNT(*) as count,
       AVG(velocity) as avg_velocity,
       MAX(velocity) as max_velocity
FROM aircraft
WHERE last_updated >= NOW() - INTERVAL 1 HOUR
  AND velocity IS NOT NULL
GROUP BY region
ORDER BY avg_velocity DESC;

-- Активные запретные зоны
SELECT name, airspaceType, 
       lowerLimitValue, upperLimitValue,
       startDateTime, endDateTime
FROM points
WHERE isActive = 1
  AND (endDateTime IS NULL OR endDateTime >= NOW())
ORDER BY name;
```

---

## 🛠️ API интеграция

### OpenSky Network

**Эндпоинт:** `https://opensky-network.org/api/states/all`

**Параметры запроса:**
- `lamin` — минимальная широта
- `lamax` — максимальная широта
- `lomin` — минимальная долгота
- `lomax` — максимальная долгота

**Лимиты:**
- Без аутентификации: 10 запросов/минуту
- С аутентификацией: 4000 запросов/день

**Документация:** https://openskynetwork.github.io/opensky-api/

### SkyArc API

**Эндпоинт:** `https://skyarc.ru/features/atpoint`

**Параметры:**
- `lat` — широта точки
- `lng` — долгота точки

**Возвращает:**
GeoJSON с информацией о зонах в указанной точке

---

## 📈 Производительность

| Метрика | Значение |
|---------|----------|
| **Частота обновления** | 600-3600 секунд |
| **Время запроса OpenSky** | 2-5 секунд |
| **Обработка данных** | 1-3 секунды |
| **Сохранение в БД** | <1 секунда |
| **Использование памяти** | 100-300 МБ |
| **Количество самолетов** | 100-500 над Россией |

### Оптимизация

- **R-Tree индекс** для быстрой геопривязки (O(log n))
- **Пул соединений** для минимизации overhead
- **Batch операции** для массовых вставок
- **Кеширование полигонов** регионов
- **Prepared geometries** для ускорения проверок

---

## 🔧 Troubleshooting

### Проблема: Нет данных от OpenSky

**Решение:**
1. Проверьте подключение к интернету
2. Тест API: `python -c "from aircraft.opensky_client import OpenSkyClient; OpenSkyClient().test_connection()"`
3. Проверьте лимиты запросов
4. Увеличьте интервал обновления

### Проблема: Неверная геопривязка

**Решение:**
1. Проверьте полигоны регионов: `SELECT COUNT(*) FROM regions`
2. Перезагрузите кеш: перезапустите приложение
3. Проверьте R-Tree индекс

### Проблема: Устаревшие данные не удаляются

**Решение:**
```python
from aircraft.aircraft import AircraftDataProcessor, DatabaseManager

processor = AircraftDataProcessor(DatabaseManager(DB_CONFIG))
processor.clear_old_data()
```

### Проблема: Потеря соединения с БД

**Решение:**
- Увеличьте `connect_timeout` в DB_CONFIG
- Проверьте пул соединений: он автоматически восстанавливается
- Проверьте логи на ошибки MySQL

---

## 🔐 Безопасность

- **Connection pooling** для защиты от exhaustion
- **Prepared statements** против SQL injection
- **Timeout** для запросов API (30 секунд)
- **Error handling** для graceful degradation
- **Retry logic** с экспоненциальным backoff

---

## 📝 Логирование

Все операции логируются в `log.log`:

```
2025-10-19 12:00:00 - INFO - Запрос данных с OpenSky Network...
2025-10-19 12:00:03 - INFO - Получено 234 самолетов
2025-10-19 12:00:04 - INFO - Обработано и сохранено: 187 записей
2025-10-19 12:00:04 - INFO - Удалено устаревших записей: 42
2025-10-19 12:00:04 - INFO - ✅ Обновление завершено
```

---

## 🤝 Интеграция с другими модулями

### С Parser Module

Комбинирование исторических данных с real-time:

```python
# Обработка исторических данных
from parser.parser_file import FlightDataProcessor
processor = FlightDataProcessor()
processor.process_all_files()

# Сбор данных в реальном времени
from aircraft.aircraft import Scheduler
scheduler.start_aircraft_data_thread()
```

### С Grid Generator

Обновление гексагонов с учетом real-time данных:

```python
from grid.grid_generator import GridGenerator

generator = GridGenerator(DB_CONFIG)
generator.update_aircraft_hexagon_ids()
```

---

## 👨‍💻 Разработка

### Добавление нового источника данных

1. Создайте класс-клиент (аналог `OpenSkyClient`)
2. Реализуйте метод `get_all_aircrafts()`
3. Добавьте обработку в `AircraftDataProcessor`
4. Обновите тесты

### Расширение обработки зон

1. Добавьте поля в таблицу `points`
2. Обновите `polygon_processor.py`
3. Добавьте новые проверки в `determine_region()`

---

## 📄 Лицензия

Проприетарное программное обеспечение. Все права защищены © 2025 Команда Finance.

---

**Дата:** 19 октября 2025  
**Версия документации:** 1.0.0  
**Модуль:** Aircraft

