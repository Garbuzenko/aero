# Модуль генерации площадок для БПЛА

## Описание

Модуль для автоматической генерации оптимальных площадок для беспилотных авиационных систем (БАС) на территории России в рамках национального проекта «Беспилотные авиационные системы» (2024-2030).

**Цель:** Создание 290 посадочных площадок к 2030 году.

## Структура таблицы

```sql
CREATE TABLE area_bpla (
    id INT AUTO_INCREMENT PRIMARY KEY,
    center_lat DECIMAL(11, 8) NOT NULL,
    center_lon DECIMAL(11, 8) NOT NULL,
    total_flights INT DEFAULT 0,
    hexagon_id INT,
    rating FLOAT NOT NULL,
    region_id INT,
    year INT COMMENT 'Год ввода в эксплуатацию (2026-2030)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Использование

### Запуск генерации

**Windows:**
```bash
py generate_area_bpla.py
```

**Linux/macOS:**
```bash
python generate_area_bpla.py
```

### Из Python кода

```python
import sys
sys.path.append('..')
from settings import DB_CONFIG
from area_bpla.generate_area_bpla import AreaBPLAGenerator

generator = AreaBPLAGenerator(DB_CONFIG)
generator.run()
```

## Настройки

Количество площадок для генерации задается в таблице `settings`:

```sql
-- Установить целевое количество площадок
INSERT INTO settings (key_name, value, description)
VALUES ('count_area_bpla', '290', 'Целевое количество площадок для БПЛА')
ON DUPLICATE KEY UPDATE value = '290';
```

По умолчанию: **290 площадок**

## Алгоритм (улучшенный)

1. **Сбор данных**
   - Гексагоны с трафиком из `grid_hexagon`
   - Запретные зоны из `points` (isActive = 1)
   - Аэропорты из `points` (поиск по ключевым словам)

2. **Расчет рейтинга (многофакторный)**
   - **40%** - Трафик БПЛА в радиусе 100 км
   - **30%** - Региональные квоты и баланс
   - **20%** - Равномерность покрытия территории
   - **10%** - Близость к аэропортам (10-30 км)

3. **Региональные ограничения**
   - Минимум 1 площадка на регион (при трафике > 50)
   - Максимум 15 площадок на один регион
   - Бонус +1000 за первую площадку в регионе
   - Штраф -800 за превышение 10 площадок в регионе

4. **Выбор локаций**
   - Сортировка по рейтингу
   - Проверка минимального расстояния ≥ 50 км
   - Контроль региональных квот

5. **Распределение по годам**
   - Площадки с высоким рейтингом → 2026
   - Площадки с низким рейтингом → 2030

6. **Сохранение** - запись в таблицу `area_bpla`

## Параметры

### Основные
- **Количество площадок:** 290 (из `settings.count_area_bpla`)
- **Минимальное расстояние:** 50 км между площадками
- **Радиус поиска трафика:** 100 км

### Веса факторов
- **Трафик БПЛА:** 40% (0.4)
- **Региональные квоты:** 30%
- **Равномерность:** 20%
- **Близость к аэропортам:** 10%

### Региональные квоты
- **Минимум на регион:** 1 площадка (если трафик > 50)
- **Максимум на регион:** 15 площадок

### Бонусы и штрафы
- **Первая площадка в регионе:** +1000
- **Недостаточное покрытие (< 3):** +500
- **Избыточное покрытие (> 10):** -800
- **Близость к аэропорту (10-30 км):** +300
- **Запретная зона:** -10,000

## Анализ результатов

```sql
-- Общая статистика
SELECT COUNT(*) as total_sites,
       SUM(total_flights) as total_traffic,
       AVG(rating) as avg_rating
FROM area_bpla;

-- Топ-10 площадок
SELECT * FROM area_bpla ORDER BY rating DESC LIMIT 10;

-- По годам
SELECT year, COUNT(*) as sites, AVG(rating) as avg_rating
FROM area_bpla
GROUP BY year
ORDER BY year;

-- По регионам
SELECT r.name, COUNT(*) as sites
FROM area_bpla a
JOIN regions r ON a.region_id = r.id
GROUP BY r.name
ORDER BY sites DESC;

-- Площадки на 2026 год (лучшие по рейтингу)
SELECT * FROM area_bpla WHERE year = 2026 ORDER BY rating DESC;

-- Региональный баланс
SELECT r.name, COUNT(*) as sites, 
       AVG(a.rating) as avg_rating,
       SUM(a.total_flights) as total_traffic
FROM area_bpla a
JOIN regions r ON a.region_id = r.id
GROUP BY r.name
ORDER BY sites DESC;

-- Проверка региональных ограничений
SELECT region_id, COUNT(*) as sites
FROM area_bpla
GROUP BY region_id
HAVING COUNT(*) > 15  -- Превышение лимита
ORDER BY sites DESC;
```

## Зависимости

- `mysql-connector-python >= 8.0.0`
- `shapely >= 2.0.0`

Все зависимости указаны в корневом `requirements.txt`.

## Версия

1.0.0 (19.10.2025)
