# 🌍 OpenStreetMap Module — Модуль загрузки границ регионов

## 📖 Описание

Модуль **OpenStreetMap** обеспечивает автоматическую загрузку административных границ России из OpenStreetMap через Overpass API. Загружает полигоны федеральных округов, субъектов Федерации и муниципальных образований с последующим сохранением в базу данных.

## 🎯 Назначение

Модуль решает следующие задачи:

- ✅ **Загрузка административных границ** России из OSM
- ✅ **Поддержка нескольких уровней** административного деления
- ✅ **Конвертация в GeoJSON** и специализированные форматы
- ✅ **Расчет площади** регионов в км²
- ✅ **Определение центроидов** для каждого региона
- ✅ **Извлечение метаданных** (название, население, Wikidata)
- ✅ **Упрощение полигонов** для оптимизации хранения

---

## 📁 Структура модуля

```
openstreetmap/
├── openstreetmap.py    # Основной скрипт загрузки
├── combined_code.txt   # Архив кода (опционально)
└── README.md          # Документация модуля (этот файл)
```

---

## 🔧 Компоненты модуля

### Основные функции

#### 1. fetch_osm_data()

Получение данных из Overpass API:

```python
def fetch_osm_data(admin_level: str) -> Optional[Dict]:
    """
    Загружает административные границы из OSM
    
    Args:
        admin_level: уровень административного деления (4, 6, 8)
        
    Returns:
        JSON ответ от Overpass API или None при ошибке
    """
```

**Overpass запрос:**
```overpass
[out:json][timeout:600];
rel["ISO3166-1"="RU"]["admin_level"="2"];
map_to_area;
rel(area)["boundary"="administrative"]["admin_level"="{level}"];
out geom;
```

**Параметры:**
- `timeout:600` — максимальное время выполнения запроса (10 минут)
- `ISO3166-1=RU` — фильтрация по России
- `admin_level` — уровень административного деления

#### 2. process_and_save_to_db()

Обработка и сохранение данных в БД:

```python
def process_and_save_to_db(geojson_data: Dict, admin_level: str):
    """
    Обрабатывает GeoJSON и сохраняет в базу данных
    
    Args:
        geojson_data: конвертированные данные в формате GeoJSON
        admin_level: уровень административного деления
    """
```

**Обработка включает:**
1. Валидация геометрии (Polygon/MultiPolygon)
2. Упрощение полигонов (tolerance=0.001)
3. Расчет центроида
4. Расчет площади в км²
5. Извлечение метаданных
6. Сохранение в БД

#### 3. extract_geopolygon_coords()

Конвертация в формат для DataLens:

```python
def extract_geopolygon_coords(geom: dict) -> Optional[list]:
    """
    Преобразует GeoJSON-геометрию в формат GEOPOLYGON для DataLens
    
    Args:
        geom: GeoJSON геометрия (Polygon или MultiPolygon)
        
    Returns:
        Список колец [[lat, lon], ...] или None при ошибке
    """
```

**Формат выхода:**
```json
[
    [[55.75, 37.61], [55.76, 37.62], ...],  // Внешнее кольцо
    [[55.74, 37.60], [55.73, 37.59], ...]   // Дырка (если есть)
]
```

#### 4. calculate_area_km2()

Расчет площади региона:

```python
def calculate_area_km2(geom) -> float:
    """
    Рассчитывает площадь полигона в км²
    
    Args:
        geom: GeoJSON геометрия
        
    Returns:
        Площадь в км²
    """
```

**Формула:**
```
area_km² = area_degrees² × (111.0 км/градус)²
```

#### 5. get_admin_type()

Определение типа административной единицы:

```python
def get_admin_type(admin_level: str) -> str:
    """
    Возвращает название типа по уровню admin_level
    
    Маппинг:
        2 - Страна
        4 - Федеральный округ
        6 - Субъект Федерации
        8 - Муниципальный район
        ...
    """
```

---

## 🗄️ База данных

### Таблица `admin_boundaries`

Основная таблица для хранения административных границ:

```sql
CREATE TABLE admin_boundaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Идентификация
    osm_id BIGINT NOT NULL,
    name VARCHAR(250) NOT NULL,
    name_en VARCHAR(250),
    
    -- Административное деление
    admin_level VARCHAR(10) NOT NULL,
    admin_type VARCHAR(100),
    boundary_type VARCHAR(50) DEFAULT 'administrative',
    place_type VARCHAR(50),
    
    -- Демография
    population INT DEFAULT 0,
    
    -- Внешние ссылки
    wikidata_id VARCHAR(20),
    wikipedia_url VARCHAR(255),
    
    -- Геометрия
    polygon_coordinates LONGTEXT,  -- Полный GeoJSON
    polygon JSON,                   -- Упрощенный полигон для DataLens
    
    -- Центроид и площадь
    centroid_lat DECIMAL(10,7),
    centroid_lon DECIMAL(10,7),
    area_sq_km DECIMAL(12,2),
    
    -- Служебные поля
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Индексы
    INDEX idx_osm_id (osm_id),
    INDEX idx_admin_level (admin_level),
    INDEX idx_name (name),
    INDEX idx_centroid (centroid_lat, centroid_lon)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 
COMMENT='Административные границы России из OpenStreetMap';
```

### Поля таблицы

| Поле | Тип | Описание |
|------|-----|----------|
| `osm_id` | BIGINT | ID объекта в OpenStreetMap |
| `name` | VARCHAR(250) | Название на русском |
| `name_en` | VARCHAR(250) | Название на английском |
| `admin_level` | VARCHAR(10) | Уровень (4, 6, 8) |
| `admin_type` | VARCHAR(100) | Тип (Федеральный округ, Субъект РФ и т.д.) |
| `population` | INT | Население (если доступно) |
| `wikidata_id` | VARCHAR(20) | ID в Wikidata (Q...) |
| `wikipedia_url` | VARCHAR(255) | Ссылка на Wikipedia |
| `polygon_coordinates` | LONGTEXT | Полный GeoJSON полигон |
| `polygon` | JSON | Упрощенный полигон для DataLens |
| `centroid_lat` | DECIMAL | Широта центра |
| `centroid_lon` | DECIMAL | Долгота центра |
| `area_sq_km` | DECIMAL | Площадь в км² |

---

## 🌐 Административные уровни

### Константа ADMIN_LEVELS

```python
ADMIN_LEVELS = {
    "federal_districts": "4",  # Федеральные округа
    "regions": "6",            # Субъекты Федерации
    "municipalities": "8"      # Муниципальные районы
}
```

### Полный маппинг уровней OSM

| Уровень | Название | Пример |
|---------|----------|--------|
| 2 | Страна | Российская Федерация |
| 3 | Международный союз | - |
| **4** | **Федеральный округ** | Центральный ФО |
| 5 | Регион (группа субъектов) | - |
| **6** | **Субъект Федерации** | Москва, Московская область |
| 7 | Городской округ | г. Королёв |
| **8** | **Муниципальный район** | Одинцовский район |
| 9 | Городское поселение | - |
| 10 | Сельское поселение | - |

---

## ⚙️ Конфигурация

### Настройки в коде

```python
# URL Overpass API
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Таймаут запросов (секунды)
TIMEOUT = 600

# Допуск упрощения полигонов
SIMPLIFY_TOLERANCE = 0.001

# Пауза между запросами (секунды)
REQUEST_DELAY = 3
```

### Настройки БД

```python
# Импортируются из settings.py
from settings import DB_CONFIG

DB_CONFIG = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': '3306',
    'database': 'aerometr',
    'charset': 'utf8mb4'
}
```

---

## 🚀 Использование

### Базовый запуск

```bash
cd openstreetmap
python openstreetmap.py
```

**Процесс:**
1. Загружает федеральные округа (admin_level=4)
2. Загружает субъекты Федерации (admin_level=6)
3. Загружает муниципальные районы (admin_level=8)
4. Сохраняет все в таблицу `admin_boundaries`

**Вывод:**
```
🌍 Загрузка административных границ России в admin_boundaries
======================================================================

📥 Уровень: federal_districts (admin_level=4)
2025-10-19 12:00:00 - INFO - 📡 Запрос уровня 4 к Overpass API...
2025-10-19 12:00:15 - INFO - ✅ Успешно сохранено 8 объектов уровня 4

📥 Уровень: regions (admin_level=6)
2025-10-19 12:00:18 - INFO - 📡 Запрос уровня 6 к Overpass API...
2025-10-19 12:01:45 - INFO - ✅ Успешно сохранено 85 объектов уровня 6

📥 Уровень: municipalities (admin_level=8)
2025-10-19 12:01:48 - INFO - 📡 Запрос уровня 8 к Overpass API...
2025-10-19 12:05:30 - INFO - ✅ Успешно сохранено 1847 объектов уровня 8

✅ Загрузка завершена. Данные сохранены в admin_boundaries.
```

### Загрузка конкретного уровня

```python
from openstreetmap.openstreetmap import fetch_osm_data, process_and_save_to_db
import osm2geojson

# Загрузка только субъектов Федерации
raw_data = fetch_osm_data("6")

if raw_data:
    geojson_data = osm2geojson.json2geojson(raw_data)
    process_and_save_to_db(geojson_data, "6")
    print("✅ Субъекты Федерации загружены")
```

### Обновление границ

```python
import mysql.connector
from settings import DB_CONFIG

# Очистка старых данных
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Удаление границ конкретного уровня
cursor.execute("DELETE FROM admin_boundaries WHERE admin_level = %s", ("6",))
conn.commit()

# Загрузка свежих данных
from openstreetmap.openstreetmap import main
main()
```

### Интеграция в основной процесс

```python
# main.py
from openstreetmap.openstreetmap import main as load_boundaries

def initialize_regions():
    """Первичная загрузка границ"""
    print("Загрузка административных границ из OSM...")
    load_boundaries()
    print("✅ Границы загружены")

if __name__ == "__main__":
    # Запускается один раз при первичной настройке
    initialize_regions()
```

---

## 📊 Примеры данных

### Пример записи в admin_boundaries

```json
{
    "osm_id": 147166,
    "name": "Москва",
    "name_en": "Moscow",
    "admin_level": "6",
    "admin_type": "Субъект Федерации",
    "boundary_type": "administrative",
    "population": 12655050,
    "wikidata_id": "Q649",
    "wikipedia_url": "ru:Москва",
    "centroid_lat": 55.755773,
    "centroid_lon": 37.617761,
    "area_sq_km": 2561.50,
    "polygon": [
        [[55.574, 37.200], [55.575, 37.201], ...],
        [[55.573, 37.199], ...]
    ]
}
```

---

## 🔍 Анализ данных

### SQL-запросы для работы с границами

#### Список всех регионов

```sql
SELECT osm_id, name, admin_type, population, area_sq_km
FROM admin_boundaries
WHERE admin_level = '6'
ORDER BY name;
```

#### Топ-10 регионов по площади

```sql
SELECT name, area_sq_km, population
FROM admin_boundaries
WHERE admin_level = '6'
ORDER BY area_sq_km DESC
LIMIT 10;
```

#### Топ-10 по населению

```sql
SELECT name, population, area_sq_km,
       ROUND(population / area_sq_km, 2) as density
FROM admin_boundaries
WHERE admin_level = '6'
  AND population > 0
ORDER BY population DESC
LIMIT 10;
```

#### Федеральные округа

```sql
SELECT name, name_en, area_sq_km
FROM admin_boundaries
WHERE admin_level = '4'
ORDER BY name;
```

#### Поиск по названию

```sql
SELECT name, admin_type, centroid_lat, centroid_lon
FROM admin_boundaries
WHERE name LIKE '%Московск%'
ORDER BY admin_level, name;
```

---

## 🗺️ Интеграция с другими модулями

### С Parser Module

Использование границ для геопривязки полетов:

```python
from parser.parser_file import FlightDataProcessor

# Парсер автоматически использует границы из БД
processor = FlightDataProcessor()
processor.load_regions()  # Загружает полигоны из admin_boundaries
```

### С Aircraft Module

Определение региона для самолета:

```python
from aircraft.aircraft import load_regions

# Загрузка полигонов регионов
load_regions()

# Определение региона по координатам
region = determine_region(55.7558, 37.6173)
print(f"Регион: {region}")  # Москва
```

### Миграция данных

Если используется таблица `regions`:

```sql
-- Копирование данных из admin_boundaries в regions
INSERT INTO regions (name, polygon, center_lat, center_lon, area_sq_km)
SELECT 
    name,
    polygon_coordinates,
    centroid_lat,
    centroid_lon,
    area_sq_km
FROM admin_boundaries
WHERE admin_level = '6';
```

---

## 🛠️ Troubleshooting

### Проблема: Timeout при запросе

**Симптом:** `RequestException: Timeout`

**Решение:**
1. Увеличьте timeout в запросе: `[timeout:900]`
2. Загружайте уровни по отдельности
3. Используйте другой экземпляр Overpass API

**Альтернативные серверы:**
```python
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter"
]
```

### Проблема: Нет данных для региона

**Симптом:** Некоторые регионы не загружаются

**Решение:**
1. Проверьте название в OSM: https://www.openstreetmap.org/
2. Убедитесь, что admin_level корректный
3. Проверьте теги `boundary=administrative`

### Проблема: Невалидная геометрия

**Симптом:** `GeometryError: Invalid geometry`

**Решение:**
```python
from shapely.geometry import shape
from shapely.validation import make_valid

shp = shape(geom)
if not shp.is_valid:
    shp = make_valid(shp)  # Автоматическое исправление
```

### Проблема: Слишком большие полигоны

**Симптом:** Ошибка при сохранении в БД (LONGTEXT overflow)

**Решение:**
1. Увеличьте упрощение: `simplify(0.01)`
2. Используйте MEDIUMTEXT или LONGTEXT для polygon_coordinates
3. Сохраняйте только упрощенную версию

---

## 📈 Производительность

| Операция | Время | Объектов |
|----------|-------|----------|
| **Загрузка уровня 4** | ~15 сек | 8 |
| **Загрузка уровня 6** | ~90 сек | 85 |
| **Загрузка уровня 8** | ~240 сек | 1,847 |
| **Обработка и сохранение** | ~5 сек | на 100 объектов |
| **Полная загрузка** | ~6 минут | 1,940 объектов |

### Оптимизация

```python
# Увеличение batch size для массовых вставок
cursor.executemany(insert_query, batch_data)

# Отключение индексов на время загрузки
cursor.execute("ALTER TABLE admin_boundaries DISABLE KEYS")
# ... загрузка данных ...
cursor.execute("ALTER TABLE admin_boundaries ENABLE KEYS")
```

---

## 🔐 Безопасность

- **SQL Injection защита**: Prepared statements
- **Валидация геометрии**: Проверка на is_valid
- **Обработка ошибок**: Try-except блоки
- **Timeout**: Ограничение времени запросов
- **Кодировка**: UTF-8 для корректной обработки русских названий

---

## 📝 Логирование

Логи сохраняются в `../log/russia_boundaries_loader.log`:

```
2025-10-19 12:00:00 - INFO - 📡 Запрос уровня 6 к Overpass API...
2025-10-19 12:01:30 - INFO - ✅ Успешно сохранено 85 объектов уровня 6
2025-10-19 12:01:31 - WARNING - ⚠️ Ошибка вставки объекта 147166: Duplicate entry
```

---

## 🌐 Внешние ресурсы

### Overpass API

- **Документация**: https://wiki.openstreetmap.org/wiki/Overpass_API
- **Overpass Turbo**: https://overpass-turbo.eu/ (визуальный редактор запросов)
- **Справка по запросам**: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL

### OpenStreetMap

- **Главная**: https://www.openstreetmap.org/
- **Wiki**: https://wiki.openstreetmap.org/
- **Taginfo**: https://taginfo.openstreetmap.org/ (справка по тегам)

### Библиотеки

- **osm2geojson**: https://github.com/aspectumapp/osm2geojson
- **Shapely**: https://shapely.readthedocs.io/

---

## 🧪 Тестирование

### Тест запроса к Overpass

```python
import requests

query = """
[out:json][timeout:25];
rel["ISO3166-1"="RU"]["admin_level"="2"];
map_to_area;
rel(area)["boundary"="administrative"]["admin_level"="6"]["name"="Москва"];
out geom;
"""

response = requests.post(
    "https://overpass-api.de/api/interpreter",
    data=query.encode('utf-8'),
    headers={'Content-Type': 'text/plain; charset=utf-8'},
    timeout=30
)

print(response.status_code)
print(len(response.json()['elements']))
```

### Проверка данных в БД

```sql
-- Количество объектов по уровням
SELECT admin_level, admin_type, COUNT(*) as count
FROM admin_boundaries
GROUP BY admin_level, admin_type
ORDER BY admin_level;

-- Регионы без координат центра
SELECT name, admin_level
FROM admin_boundaries
WHERE centroid_lat IS NULL OR centroid_lon IS NULL;

-- Регионы с нулевой площадью
SELECT name, admin_level, area_sq_km
FROM admin_boundaries
WHERE area_sq_km = 0 OR area_sq_km IS NULL;
```

---

## 📄 Лицензия

Данные OpenStreetMap предоставляются под лицензией **ODbL** (Open Database License).

**Требования:**
- © OpenStreetMap contributors
- Указание источника данных при использовании
- Share-Alike при распространении

**Подробнее:** https://www.openstreetmap.org/copyright

Программное обеспечение: Проприетарное © 2025 Команда Finance.

---

## 🔄 Обновление данных

### Периодичность обновления

Рекомендуется обновлять границы:
- **Федеральные округа (уровень 4)**: раз в год
- **Субъекты Федерации (уровень 6)**: раз в 3-6 месяцев
- **Муниципалитеты (уровень 8)**: раз в месяц

### Автоматизация обновления

```python
# cron job или scheduled task
from openstreetmap.openstreetmap import main
import schedule
import time

def update_boundaries():
    print("Обновление административных границ...")
    main()
    print("✅ Обновление завершено")

# Запуск раз в месяц
schedule.every().month.do(update_boundaries)

while True:
    schedule.run_pending()
    time.sleep(86400)  # Проверка раз в сутки
```

---

**Дата:** 19 октября 2025  
**Версия документации:** 1.0.0  
**Модуль:** OpenStreetMap

