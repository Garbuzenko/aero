# 🗄️ DataBase — Схема базы данных

## 📖 Описание

Папка **DataBase** содержит SQL-дампы и схемы базы данных проекта АЭРОМЕТР. Используется для развертывания, резервного копирования и миграции базы данных.

## 📁 Структура

```
DataBase/
├── u3253297_hack.sql    # Полный дамп базы данных
└── README.md            # Документация (этот файл)
```

---

## 🗄️ База данных

### Информация о БД

- **СУБД**: MySQL 8.0+
- **Кодировка**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Размер**: ~200+ MB (дамп)
- **Таблиц**: 15+

---

## 📊 Основные таблицы

### 1. Данные о полетах

#### `processed_flights`
Обработанные данные о полетах БПЛА

**Ключевые поля:**
- `id` — уникальный идентификатор
- `dof_date` — дата полета
- `atd_time`, `ata_time` — время вылета/прилета
- `duration_min` — длительность в минутах
- `departure_coords`, `arrival_coords` — координаты
- `departure_region`, `arrival_region` — регионы
- `operator` — оператор полета
- `aircraft_type_code` — тип БПЛА
- `altitude_max` — максимальная высота
- `hexagon_id` — привязка к гексагону H3
- `prediction` — тип данных (download/prediction)

**Индексы:**
- `idx_dof_date` — по дате
- `idx_region_id` — по региону
- `idx_hexagon_id` — по гексагону
- `idx_filename` — по файлу источнику

---

### 2. Географические данные

#### `regions`
Регионы России с границами

**Поля:**
- `id` — ID региона
- `name` — название региона
- `polygon` — полигон границы (GeoJSON)
- `center_lat`, `center_lon` — координаты центра
- `area_sq_km` — площадь в км²

#### `grid_hexagon`
Гексагональная сетка H3 (разрешение 6)

**Поля:**
- `id` — ID
- `hexagon_index` — уникальный H3 индекс
- `center_lat`, `center_lon` — центр гексагона
- `total_flights` — количество полетов
- `region_id` — привязка к региону

#### `grid_square`
Квадратная сетка

**Поля:**
- `id` — ID
- `min_lat`, `max_lat`, `min_lon`, `max_lon` — границы
- `center_lat`, `center_lon` — центр
- `total_flights` — количество полетов
- `region_id` — привязка к региону

---

### 3. Статистика

#### `region_stats`
Ежедневная статистика по регионам

**Поля:**
- `region` — название региона
- `region_id` — ID региона
- `date` — дата
- `prediction` — тип данных (download/prediction)
- `total_flights` — всего полетов
- `peak_load` — пиковая нагрузка (полетов/час)
- `flight_density` — плотность на 1000 км²
- `morning_flights`, `afternoon_flights`, `evening_flights`, `night_flights` — распределение по времени суток
- `avg_duration_min` — средняя длительность
- `zero_days` — дней без полетов подряд

#### `region_stats_month`
Месячная агрегированная статистика

**Поля:**
- `region` — название региона
- `month` — месяц (YYYY-MM)
- `prediction` — тип данных
- `total_flights` — всего полетов
- `avg_flight_duration` — средняя длительность
- `monthly_change` — изменение относительно прошлого месяца (%)
- `morning_percent`, `afternoon_percent`, `evening_percent`, `night_percent` — проценты по времени суток
- `median_daily_flights` — медиана ежедневных полетов

---

### 4. Real-time данные

#### `aircraft`
Воздушные суда в реальном времени (OpenSky Network)

**Поля:**
- `id` — ID записи
- `icao24` — ICAO24 код
- `callsign` — позывной
- `latitude`, `longitude` — координаты
- `baro_altitude` — высота (м)
- `velocity` — скорость (м/с)
- `region`, `region_id` — регион
- `last_updated` — время обновления

**Особенности:**
- Автоматическая очистка данных старше 24 часов
- Обновление каждые 600-3600 секунд

---

### 5. Площадки для БПЛА

#### `area_bpla`
Оптимальные площадки для посадки БПЛА (290 шт.)

**Поля:**
- `id` — ID площадки
- `center_lat`, `center_lon` — координаты
- `total_flights` — трафик в зоне
- `hexagon_id` — привязка к гексагону
- `rating` — рейтинг локации
- `region_id` — регион

---

### 6. Запретные зоны

#### `points`
Запретные зоны и ограничения полетов (SkyArc)

**Поля:**
- `id` — ID зоны
- `name` — название
- `polygon` — полигон зоны (JSON)
- `startDateTime`, `endDateTime` — временные ограничения
- `airspaceType` — тип воздушного пространства
- `lowerLimit`, `upperLimit` — высотные ограничения
- `isActive` — активна ли зона

---

### 7. Служебные таблицы

#### `processed_files`
Отслеживание обработки Excel файлов

**Поля:**
- `filename` — имя файла
- `status` — статус (pending/processing/processed/error)
- `procent` — процент обработки
- `error_message` — сообщение об ошибке

#### `settings`
Настройки системы

**Поля:**
- `key_name` — ключ настройки
- `value` — значение
- `description` — описание

**Примеры настроек:**
```sql
grid_cell_area = 1000          # Площадь ячейки сетки (км²)
count_area_bpla = 290          # Количество площадок БПЛА
start_date = 2024-01-01        # Начало периода обработки
end_date = 2025-12-31          # Конец периода
start_date_prediction = ...    # Начало прогнозного периода
```

---

### 8. Административные границы

#### `admin_boundaries`
Административные границы из OpenStreetMap

**Поля:**
- `osm_id` — ID в OSM
- `name`, `name_en` — название (рус/англ)
- `admin_level` — уровень (4=ФО, 6=Субъект, 8=Район)
- `admin_type` — тип административной единицы
- `polygon_coordinates` — полный GeoJSON
- `polygon` — упрощенный полигон для DataLens
- `centroid_lat`, `centroid_lon` — центр
- `area_sq_km` — площадь
- `population` — население

---

## 🚀 Использование

### Импорт дампа

#### Полный импорт

```bash
# MySQL
mysql -u username -p aerometr < DataBase/u3253297_hack.sql

# Или через source
mysql -u username -p
> USE aerometr;
> SOURCE DataBase/u3253297_hack.sql;
```

#### С прогресс-баром (Linux/Mac)

```bash
pv DataBase/u3253297_hack.sql | mysql -u username -p aerometr
```

### Частичный импорт

#### Только структура (без данных)

```bash
# Извлечение только CREATE TABLE
grep -E "(CREATE TABLE|CREATE INDEX|DROP TABLE)" DataBase/u3253297_hack.sql > schema_only.sql
mysql -u username -p aerometr < schema_only.sql
```

#### Конкретная таблица

```bash
# Извлечение таблицы processed_flights
sed -n '/CREATE TABLE.*processed_flights/,/ENGINE=/p' DataBase/u3253297_hack.sql > processed_flights.sql
mysql -u username -p aerometr < processed_flights.sql
```

---

## 🔧 Настройка базы данных

### Создание БД

```sql
-- Создание базы данных
CREATE DATABASE aerometr 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

-- Создание пользователя
CREATE USER 'aerometr_user'@'localhost' IDENTIFIED BY 'secure_password';

-- Выдача прав
GRANT ALL PRIVILEGES ON aerometr.* TO 'aerometr_user'@'localhost';
FLUSH PRIVILEGES;
```

### Оптимизация

```sql
-- Увеличение размера буфера для импорта
SET GLOBAL max_allowed_packet=1073741824;  -- 1GB

-- Отключение проверок для ускорения импорта
SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
SET AUTOCOMMIT=0;

-- Импорт данных
SOURCE DataBase/u3253297_hack.sql;

-- Включение проверок обратно
COMMIT;
SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
SET AUTOCOMMIT=1;
```

---

## 💾 Резервное копирование

### Создание дампа

#### Полный дамп

```bash
# С данными
mysqldump -u username -p \
  --single-transaction \
  --routines \
  --triggers \
  --databases aerometr > aerometr_backup_$(date +%Y%m%d).sql

# Только структура
mysqldump -u username -p \
  --no-data \
  --databases aerometr > aerometr_schema_$(date +%Y%m%d).sql
```

#### Сжатый дамп

```bash
# С компрессией gzip
mysqldump -u username -p aerometr | gzip > aerometr_$(date +%Y%m%d).sql.gz

# С компрессией xz (лучше, но медленнее)
mysqldump -u username -p aerometr | xz > aerometr_$(date +%Y%m%d).sql.xz
```

#### Через Python (модуль backup.py)

```python
from backup import BackupCreator
from settings import DB_CONFIG

creator = BackupCreator(DB_CONFIG)
backup_file = creator.create_backup()
print(f"✅ Бэкап создан: {backup_file}")
```

---

## 📈 Статистика базы данных

### Размер таблиц

```sql
SELECT 
    table_name AS "Table",
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)",
    table_rows AS "Rows"
FROM information_schema.TABLES
WHERE table_schema = 'aerometr'
ORDER BY (data_length + index_length) DESC;
```

### Статус индексов

```sql
SELECT 
    table_name,
    index_name,
    non_unique,
    seq_in_index,
    column_name
FROM information_schema.statistics
WHERE table_schema = 'aerometr'
ORDER BY table_name, index_name, seq_in_index;
```

### Фрагментация

```sql
SELECT 
    table_name,
    ROUND(data_free / 1024 / 1024, 2) AS "Fragmentation (MB)"
FROM information_schema.tables
WHERE table_schema = 'aerometr'
  AND data_free > 0
ORDER BY data_free DESC;
```

---

## 🔍 Миграции

### Структура миграций (рекомендация)

```
DataBase/
├── u3253297_hack.sql           # Полный дамп
├── migrations/
│   ├── 001_initial_schema.sql
│   ├── 002_add_hexagon_id.sql
│   ├── 003_add_predictions.sql
│   └── ...
└── schema/
    ├── tables/
    │   ├── processed_flights.sql
    │   ├── regions.sql
    │   └── ...
    └── indexes/
        ├── idx_processed_flights.sql
        └── ...
```

### Пример миграции

```sql
-- migrations/002_add_hexagon_id.sql

-- Добавление поля hexagon_id в processed_flights
ALTER TABLE processed_flights
ADD COLUMN hexagon_id INT,
ADD INDEX idx_hexagon_id (hexagon_id);

-- Обновление существующих записей
UPDATE processed_flights pf
INNER JOIN grid_hexagon gh 
  ON ST_Contains(gh.polygon, POINT(pf.start_lon, pf.start_lat))
SET pf.hexagon_id = gh.id
WHERE pf.hexagon_id IS NULL;
```

---

## 🛠️ Troubleshooting

### Проблема: Ошибка импорта "max_allowed_packet"

**Решение:**
```sql
SET GLOBAL max_allowed_packet=1073741824;  -- 1GB
```

Или в my.cnf:
```ini
[mysqld]
max_allowed_packet=1G
```

### Проблема: Медленный импорт

**Решение:**
```sql
-- Отключите проверки
SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
SET AUTOCOMMIT=0;

-- Выполните импорт

-- Включите обратно
COMMIT;
SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
```

### Проблема: Нехватка места на диске

**Решение:**
1. Очистите старые логи: `rm /var/log/mysql/*.log`
2. Удалите временные таблицы
3. Оптимизируйте таблицы: `OPTIMIZE TABLE table_name;`

---

## 📊 Мониторинг

### Активные запросы

```sql
SHOW FULL PROCESSLIST;
```

### Медленные запросы

```sql
-- Включить лог медленных запросов
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  -- Запросы > 2 сек

-- Просмотр
SELECT * FROM mysql.slow_log;
```

### Статус сервера

```sql
SHOW STATUS;
SHOW VARIABLES;
```

---

## 🔐 Безопасность

### Рекомендации

1. **Не храните дампы в открытом доступе**
2. **Используйте сильные пароли** для БД
3. **Регулярное резервное копирование** (ежедневно)
4. **Шифрование дампов**:
   ```bash
   mysqldump aerometr | gpg -c > aerometr.sql.gpg
   ```
5. **Ограничение прав пользователей**:
   ```sql
   GRANT SELECT, INSERT, UPDATE, DELETE ON aerometr.* TO 'app_user'@'localhost';
   ```

---

## 📝 Changelog

### Версия 1.0.0 (2025-10-19)
- ✅ Полная схема базы данных
- ✅ Все основные таблицы
- ✅ Индексы и ограничения
- ✅ Поддержка прогнозных данных
- ✅ H3 гексагональная сетка
- ✅ Площадки для БПЛА

---

## 📄 Лицензия

Проприетарное программное обеспечение. Все права защищены © 2025 Команда Finance.

---

**Дата:** 19 октября 2025  
**Версия документации:** 1.0.0  
**База данных:** MySQL 8.0+

