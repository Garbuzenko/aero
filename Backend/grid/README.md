# 🗺️ Grid Generator — Модуль генерации пространственных сеток

## 📖 Описание

Модуль **Grid Generator** обеспечивает создание и управление пространственными сетками для территории России. Генерирует квадратные и гексагональные (H3) сетки, рассчитывает плотность полетов по ячейкам и выполняет геопривязку данных к ячейкам сетки.

## 🎯 Назначение

Модуль решает следующие задачи:

- ✅ **Генерация квадратных сеток** заданной площади
- ✅ **Генерация гексагональных сеток H3** (разрешение 6)
- ✅ **Расчет плотности полетов** по ячейкам
- ✅ **Геопривязка полетов** к ячейкам сетки
- ✅ **Фильтрация по территории** России
- ✅ **Обновление статистики** в реальном времени
- ✅ **Настраиваемая площадь** ячеек через таблицу settings

---

## 📁 Структура модуля

```
grid/
├── grid_generator.py    # Основной генератор сеток
├── __init__.py         # Инициализация модуля
└── README.md           # Документация модуля (этот файл)
```

---

## 🔧 Компоненты модуля

### GridGenerator — Основной класс

```python
class GridGenerator:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.default_area = 1000  # км² по умолчанию
        self.regions = []  # Кэш регионов России
```

#### Основные методы

##### 1. Генерация сеток

```python
def generate_grids(self, bbox: tuple) -> bool:
    """
    Генерирует квадратные и гексагональные сетки для территории
    
    Args:
        bbox: (lat_min, lon_min, lat_max, lon_max)
        
    Returns:
        True если успешно, False при ошибке
    """
```

**Пример:**
```python
from grid.grid_generator import GridGenerator
from settings import DB_CONFIG

generator = GridGenerator(DB_CONFIG)
generator.connect()

# Bbox России
russia_bbox = (41.0, 19.0, 82.0, 180.0)
if generator.generate_grids(russia_bbox):
    print("✅ Сетки успешно созданы")
```

##### 2. Квадратная сетка

```python
def generate_square_grid(self, bbox: tuple, area_km2: float) -> bool:
    """
    Генерирует квадратную сетку заданной площади
    
    Args:
        bbox: границы территории
        area_km2: площадь ячейки в км²
        
    Returns:
        True если успешно
    """
```

**Алгоритм:**
1. Рассчитывается размер стороны квадрата: `side = sqrt(area_km2)`
2. Вычисляется шаг в градусах: `lat_step = side / 111.0`
3. Генерируется сетка с учетом bbox
4. Каждая ячейка фильтруется по территории России
5. Рассчитывается количество полетов в ячейке

##### 3. Гексагональная сетка (H3)

```python
def generate_hexagon_grid(self, bbox: tuple, resolution: int = 6) -> bool:
    """
    Генерирует гексагональную сетку H3
    
    Args:
        bbox: границы территории
        resolution: разрешение H3 (0-15), по умолчанию 6
        
    Returns:
        True если успешно
    """
```

**Разрешения H3:**

| Разрешение | Размер ячейки | Площадь (км²) | Применение |
|------------|---------------|---------------|------------|
| 0 | ~1,200 км | ~4,250,000 | Континенты |
| 3 | ~60 км | ~1,000 | Страны |
| **6** | **~3.2 км** | **~36** | **Регионы (используется)** |
| 9 | ~174 м | ~0.10 | Города |
| 12 | ~9.4 м | ~0.0001 | Улицы |

**Преимущества H3:**
- Равномерное покрытие
- Одинаковая площадь ячеек
- Эффективное хранение
- Быстрый поиск соседей
- Иерархическая структура

##### 4. Обновление плотности полетов

```python
def update_grid_cell_flights(self, batch_size: int = 1000) -> bool:
    """
    Обновляет количество полетов в квадратных ячейках
    
    Args:
        batch_size: размер пакета для обновления
    """

def update_hexagon_flights(self) -> bool:
    """
    Обновляет количество полетов в гексагональных ячейках H3
    """
```

**Процесс обновления:**
1. Загружаются все полеты из `processed_flights`
2. Для каждого полета определяется ячейка сетки
3. Подсчитывается количество полетов в каждой ячейке
4. Обновляются поля `total_flights` в таблицах сеток

##### 5. Привязка полетов к гексагонам

```python
def update_processed_flights_hexagon_id_simple(self) -> int:
    """
    Обновляет hexagon_id в таблице processed_flights
    
    Returns:
        Количество обновленных записей
    """
```

**Алгоритм:**
1. Извлекаются все полеты без hexagon_id
2. Для каждого полета вычисляется H3 индекс
3. Находится соответствующая запись в `grid_hexagon`
4. Обновляется поле `hexagon_id`

##### 6. Утилиты

```python
def get_setting_value(self, key: str, default: str) -> str:
    """Получение значения настройки из таблицы settings"""

def check_table_exists(self, table_name: str) -> bool:
    """Проверка существования таблицы"""

def drop_grid_tables() -> bool:
    """Удаление таблиц сеток"""

def create_settings_table() -> bool:
    """Создание таблицы настроек"""
```

---

## 🗄️ База данных

### Таблица `grid_square`

Квадратная сетка:

```sql
CREATE TABLE grid_square (
    id INT AUTO_INCREMENT PRIMARY KEY,
    min_lat DECIMAL(10,7) NOT NULL,
    max_lat DECIMAL(10,7) NOT NULL,
    min_lon DECIMAL(10,7) NOT NULL,
    max_lon DECIMAL(10,7) NOT NULL,
    center_lat DECIMAL(10,7) NOT NULL,
    center_lon DECIMAL(10,7) NOT NULL,
    total_flights INT DEFAULT 0,
    region_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_center (center_lat, center_lon),
    INDEX idx_region (region_id),
    INDEX idx_flights (total_flights)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 
COMMENT='Квадратная сетка для анализа плотности полетов';
```

**Поля:**
- `min_lat`, `max_lat`, `min_lon`, `max_lon` — границы квадрата
- `center_lat`, `center_lon` — центр квадрата
- `total_flights` — количество полетов в ячейке
- `region_id` — ID региона

### Таблица `grid_hexagon`

Гексагональная сетка H3:

```sql
CREATE TABLE grid_hexagon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hexagon_index VARCHAR(20) UNIQUE NOT NULL,
    center_lat DECIMAL(10,7) NOT NULL,
    center_lon DECIMAL(10,7) NOT NULL,
    total_flights INT DEFAULT 0,
    region_id INT,
    resolution INT DEFAULT 6,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_hexagon_index (hexagon_index),
    INDEX idx_center (center_lat, center_lon),
    INDEX idx_region (region_id),
    INDEX idx_flights (total_flights)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 
COMMENT='Гексагональная сетка H3 для анализа плотности полетов';
```

**Поля:**
- `hexagon_index` — уникальный H3 индекс (например: "86754e64fffffff")
- `center_lat`, `center_lon` — центр гексагона
- `total_flights` — количество полетов в гексагоне
- `region_id` — ID региона
- `resolution` — разрешение H3 (обычно 6)

### Таблица `settings`

Настройки модуля:

```sql
CREATE TABLE settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key_name VARCHAR(50) UNIQUE NOT NULL,
    value VARCHAR(255) NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Площадь ячейки сетки
INSERT INTO settings (key_name, value, description)
VALUES ('grid_cell_area', '1000', 'Площадь ячейки квадратной сетки в км²');
```

### Связь с processed_flights

```sql
ALTER TABLE processed_flights 
ADD COLUMN hexagon_id INT,
ADD INDEX idx_hexagon_id (hexagon_id);
```

---

## ⚙️ Конфигурация

### Настройки по умолчанию

```python
# Разрешение H3
H3_RESOLUTION = 6  # ~36 км² на ячейку

# Площадь квадратной ячейки
DEFAULT_CELL_AREA = 1000  # км²

# Bbox России
RUSSIA_BBOX = (41.0, 19.0, 82.0, 180.0)  # (lat_min, lon_min, lat_max, lon_max)

# Размер пакета для обновлений
BATCH_SIZE = 1000
```

### Изменение площади ячейки

**Через SQL:**
```sql
UPDATE settings 
SET value = '2000' 
WHERE key_name = 'grid_cell_area';
```

**Через Python:**
```python
generator = GridGenerator(DB_CONFIG)
generator.default_area = 2000  # 2000 км²
```

### Изменение разрешения H3

```python
# Более детальная сетка (разрешение 7, ~5 км²)
generator.generate_hexagon_grid(russia_bbox, resolution=7)

# Менее детальная сетка (разрешение 5, ~252 км²)
generator.generate_hexagon_grid(russia_bbox, resolution=5)
```

---

## 🚀 Использование

### Базовая генерация сеток

```python
from grid.grid_generator import GridGenerator
from settings import DB_CONFIG

# Инициализация
generator = GridGenerator(DB_CONFIG)
generator.connect()

# Генерация обеих сеток для России
russia_bbox = (41.0, 19.0, 82.0, 180.0)
success = generator.generate_grids(russia_bbox)

if success:
    print("✅ Сетки созданы успешно")
else:
    print("❌ Ошибка создания сеток")
```

### Генерация только квадратной сетки

```python
generator = GridGenerator(DB_CONFIG)
generator.connect()

# Квадраты по 500 км²
bbox = (41.0, 19.0, 82.0, 180.0)
generator.generate_square_grid(bbox, area_km2=500)
```

### Генерация только гексагональной сетки

```python
generator = GridGenerator(DB_CONFIG)
generator.connect()

# H3 разрешение 7 (более детально)
bbox = (55.0, 37.0, 56.0, 38.0)  # Москва
generator.generate_hexagon_grid(bbox, resolution=7)
```

### Обновление статистики полетов

```python
generator = GridGenerator(DB_CONFIG)
generator.connect()

# Обновление квадратных ячеек
generator.update_grid_cell_flights()

# Обновление гексагонов
generator.update_hexagon_flights()

print("✅ Статистика обновлена")
```

### Привязка полетов к гексагонам

```python
generator = GridGenerator(DB_CONFIG)
generator.connect()

# Обновление hexagon_id в processed_flights
updated_count = generator.update_processed_flights_hexagon_id_simple()
print(f"Обновлено записей: {updated_count}")
```

### Полный цикл обработки

```python
from grid.grid_generator import GridGenerator
from settings import DB_CONFIG

def full_grid_update():
    generator = GridGenerator(DB_CONFIG)
    
    if not generator.connect():
        return False
    
    # 1. Генерация сеток
    russia_bbox = (41.0, 19.0, 82.0, 180.0)
    if not generator.generate_grids(russia_bbox):
        return False
    
    # 2. Привязка полетов к гексагонам
    updated = generator.update_processed_flights_hexagon_id_simple()
    print(f"Привязано полетов: {updated}")
    
    # 3. Обновление статистики
    generator.update_hexagon_flights()
    generator.update_grid_cell_flights()
    
    print("✅ Полное обновление завершено")
    return True

if __name__ == "__main__":
    full_grid_update()
```

---

## 📊 Анализ данных

### SQL-запросы для анализа

#### Топ ячеек по плотности полетов

```sql
-- Квадратные ячейки
SELECT 
    id,
    center_lat,
    center_lon,
    total_flights,
    region_id
FROM grid_square
ORDER BY total_flights DESC
LIMIT 20;

-- Гексагоны H3
SELECT 
    hexagon_index,
    center_lat,
    center_lon,
    total_flights,
    region_id
FROM grid_hexagon
ORDER BY total_flights DESC
LIMIT 20;
```

#### Статистика по регионам

```sql
-- Средняя плотность по регионам (гексагоны)
SELECT 
    r.name as region_name,
    COUNT(gh.id) as hexagon_count,
    SUM(gh.total_flights) as total_flights,
    AVG(gh.total_flights) as avg_flights_per_hexagon,
    MAX(gh.total_flights) as max_flights_in_hexagon
FROM grid_hexagon gh
JOIN regions r ON gh.region_id = r.id
GROUP BY r.name
ORDER BY total_flights DESC;
```

#### Горячие зоны (hotspots)

```sql
-- Зоны с высокой плотностью (>100 полетов)
SELECT 
    hexagon_index,
    center_lat,
    center_lon,
    total_flights,
    CASE 
        WHEN total_flights > 1000 THEN 'Очень высокая'
        WHEN total_flights > 500 THEN 'Высокая'
        WHEN total_flights > 100 THEN 'Средняя'
        ELSE 'Низкая'
    END as density_level
FROM grid_hexagon
WHERE total_flights > 100
ORDER BY total_flights DESC;
```

#### Покрытие территории

```sql
-- Процент покрытия (ячеек с полетами)
SELECT 
    COUNT(*) as total_cells,
    SUM(CASE WHEN total_flights > 0 THEN 1 ELSE 0 END) as cells_with_flights,
    ROUND(SUM(CASE WHEN total_flights > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as coverage_percent
FROM grid_hexagon;
```

---

## 🔍 Визуализация

### Экспорт для визуализации

```python
import json
from grid.grid_generator import GridGenerator

def export_hexagons_geojson(filename='hexagons.geojson'):
    """Экспорт гексагонов в GeoJSON"""
    import h3
    
    generator = GridGenerator(DB_CONFIG)
    generator.connect()
    
    cursor = generator.connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT hexagon_index, center_lat, center_lon, total_flights
        FROM grid_hexagon
        WHERE total_flights > 0
    """)
    
    features = []
    for row in cursor.fetchall():
        # Получаем границы гексагона
        boundary = h3.h3_to_geo_boundary(row['hexagon_index'], geo_json=True)
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [boundary]
            },
            "properties": {
                "hexagon_index": row['hexagon_index'],
                "center": [row['center_lat'], row['center_lon']],
                "flights": row['total_flights']
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Экспортировано {len(features)} гексагонов в {filename}")

export_hexagons_geojson()
```

### Визуализация в Yandex Maps

```javascript
// Загрузка и отображение гексагонов
fetch('hexagons.geojson')
    .then(response => response.json())
    .then(data => {
        data.features.forEach(feature => {
            const flights = feature.properties.flights;
            const color = getColorByFlights(flights);
            
            const polygon = new ymaps.Polygon(
                feature.geometry.coordinates,
                {
                    hintContent: `Полетов: ${flights}`
                },
                {
                    fillColor: color,
                    fillOpacity: 0.6,
                    strokeColor: '#000',
                    strokeWidth: 1
                }
            );
            
            map.geoObjects.add(polygon);
        });
    });

function getColorByFlights(flights) {
    if (flights > 1000) return '#FF0000';  // Красный
    if (flights > 500) return '#FF8800';   // Оранжевый
    if (flights > 100) return '#FFFF00';   // Желтый
    return '#00FF00';  // Зеленый
}
```

---

## 📈 Производительность

| Операция | Время | Записей |
|----------|-------|---------|
| **Генерация квадратной сетки** | 10-30 сек | ~50,000 ячеек |
| **Генерация H3 сетки** | 5-15 сек | ~30,000 гексагонов |
| **Обновление плотности** | 30-120 сек | Зависит от полетов |
| **Привязка к гексагонам** | 1-5 минут | ~100,000 полетов |
| **Использование памяти** | 200-500 МБ | - |

### Оптимизация

```python
# Увеличение размера batch для быстрой обработки
generator.update_grid_cell_flights(batch_size=5000)

# Использование индексов
# - Индексы по координатам для быстрого поиска
# - Индексы по hexagon_index для уникальности
# - Индексы по total_flights для сортировки
```

---

## 🛠️ Troubleshooting

### Проблема: Слишком много ячеек

**Симптом:** Генерация занимает >5 минут

**Решение:**
1. Увеличьте площадь ячейки: `area_km2=2000`
2. Уменьшите разрешение H3: `resolution=5`
3. Ограничьте bbox меньшей территорией

### Проблема: Ячейки вне России

**Симптом:** Множество ячеек за пределами РФ

**Решение:**
- Включена фильтрация по регионам
- Проверьте наличие полигонов в таблице `regions`
- Убедитесь, что `region_id` корректно заполнен

### Проблема: Нет данных о полетах в ячейках

**Симптом:** `total_flights = 0` для всех ячеек

**Решение:**
```python
# 1. Проверьте наличие полетов
cursor.execute("SELECT COUNT(*) FROM processed_flights")
print(f"Полетов в БД: {cursor.fetchone()[0]}")

# 2. Обновите привязку к гексагонам
generator.update_processed_flights_hexagon_id_simple()

# 3. Обновите статистику
generator.update_hexagon_flights()
```

### Проблема: Дублирование гексагонов

**Симптом:** Ошибка UNIQUE constraint на hexagon_index

**Решение:**
```sql
-- Удалите дубликаты
DELETE gh1 FROM grid_hexagon gh1
INNER JOIN grid_hexagon gh2 
WHERE gh1.id > gh2.id 
  AND gh1.hexagon_index = gh2.hexagon_index;
```

---

## 🔐 Безопасность

- **SQL Injection защита**: Prepared statements
- **Валидация входных данных**: Проверка bbox
- **Обработка ошибок**: Try-except блоки
- **Транзакции**: Rollback при ошибках
- **Логирование**: Все операции записываются

---

## 📝 Логирование

Логи сохраняются в `../log.log`:

```
2025-10-19 12:00:00 - INFO - Начало генерации сеток
2025-10-19 12:00:05 - INFO - ✅ Квадратная сетка создана: 52,341 ячеек
2025-10-19 12:00:12 - INFO - ✅ Гексагональная сетка H3 создана: 31,245 гексагонов
2025-10-19 12:00:45 - INFO - Обновлено hexagon_id: 145,678 записей
2025-10-19 12:01:30 - INFO - ✅ Статистика полетов обновлена
```

---

## 🤝 Интеграция с другими модулями

### С Parser Module

```python
# После обработки полетов обновляем сетки
from parser.parser_file import FlightDataProcessor
from grid.grid_generator import GridGenerator

processor = FlightDataProcessor()
processor.process_all_files()

# Обновление сеток
generator = GridGenerator(DB_CONFIG)
generator.connect()
generator.update_processed_flights_hexagon_id_simple()
generator.update_hexagon_flights()
```

### С Area BPLA Module

```python
# Генератор площадок использует гексагоны
from area_bpla.generate_area_bpla import AreaBPLAGenerator

# Сначала генерируем/обновляем сетки
generator = GridGenerator(DB_CONFIG)
generator.generate_grids(russia_bbox)

# Затем генерируем площадки на основе гексагонов
area_generator = AreaBPLAGenerator(DB_CONFIG)
area_generator.run()
```

---

## 📚 Дополнительные ресурсы

### H3 Документация

- **Официальный сайт**: https://h3geo.org/
- **GitHub**: https://github.com/uber/h3
- **Python библиотека**: https://github.com/uber/h3-py

### Полезные ссылки

- **H3 Explorer**: https://wolf-h3-viewer.glitch.me/ (визуализация)
- **H3 Calculator**: https://observablehq.com/@nrabinowitz/h3-index-inspector

---

## 📄 Лицензия

Проприетарное программное обеспечение. Все права защищены © 2025 Команда Finance.

---

**Дата:** 19 октября 2025  
**Версия документации:** 1.0.0  
**Модуль:** Grid Generator

