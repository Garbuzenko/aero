# 📊 DataLens — Интеграция с Yandex DataLens

## 📖 Описание

Папка **Datalens** содержит конфигурацию интеграции с **Yandex DataLens** — сервисом визуализации и аналитики данных. Включает настройки дашбордов, чартов и механизм встраивания с JWT-аутентификацией.

## 📁 Структура

```
Datalens/
├── lct.json         # Конфигурация дашбордов и чартов DataLens
├── README.md        # Документация (этот файл)
└── ../datalens.py   # Генератор JWT токенов для встраивания
```

---

## 🎯 Назначение

Модуль решает следующие задачи:

- ✅ **Визуализация данных** через Yandex DataLens
- ✅ **Встраивание дашбордов** на сайт aerometr.ru
- ✅ **JWT-аутентификация** для безопасного доступа
- ✅ **Интерактивные чарты** и графики
- ✅ **Реал-тайм обновление** данных
- ✅ **Экспорт/импорт конфигурации** дашбордов

---

## 🗂️ Файлы

### 1. lct.json

**Описание:** Полная конфигурация дашбордов DataLens в JSON формате

**Содержит:**
- Подключения к базе данных
- Датасеты (datasets)
- Чарты (charts)
- Дашборды (dashboards)
- Фильтры и параметры
- Связи между объектами

**Размер:** ~200MB (включает все визуализации)

**Формат:**
```json
{
  "dashboards": [...],
  "datasets": [...],
  "charts": [...],
  "connections": [...],
  "widgets": [...]
}
```

### 2. ../datalens.py

**Описание:** Генератор JWT токенов для встраивания дашбордов

**Код:**
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
print(encoded_token)
```

---

## 🔐 JWT-аутентификация

### Механизм работы

1. **Генерация токена** на сервере
2. **Передача токена** в iframe
3. **Проверка подписи** DataLens
4. **Отображение дашборда** пользователю

### Структура JWT payload

```json
{
  "embedId": "8e0tatm9jpjit",
  "dlEmbedService": "YC_DATALENS_EMBEDDING_SERVICE_MARK",
  "iat": 1697712345,
  "exp": 1697715945,
  "params": {
    "region_id": "77",
    "date_from": "2024-01-01",
    "date_to": "2025-12-31"
  }
}
```

**Поля:**
- `embedId` — ID встраиваемого дашборда
- `dlEmbedService` — метка сервиса DataLens
- `iat` (issued at) — время создания токена
- `exp` (expiration) — время истечения (обычно +1 час)
- `params` — параметры для фильтрации данных

### Алгоритм подписи

**PS256 (RSA-PSS with SHA-256)**
- Требуется RSA приватный ключ (PEM формат)
- Ключ хранится в `settings.py` (переменная `private_key`)

---

## 🚀 Использование

### Генерация JWT токена

#### Через Python скрипт

```bash
cd /path/to/aerometr
python datalens.py
```

**Вывод:**
```
eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWJlZElkIjoiOGUwdGF0bTlq...
```

#### Через API endpoint

```python
# app.py
@app.route('/generate_datalens_token', methods=['GET'])
def generate_datalens_token():
    import time
    now = int(time.time())
    payload = {
        'embedId': "8e0tatm9jpjit",
        'dlEmbedService': "YC_DATALENS_EMBEDDING_SERVICE_MARK",
        'iat': now,
        'exp': now + 3600,
        "params": {}
    }
    
    encoded_token = jwt.encode(payload, private_key, algorithm='PS256')
    
    return jsonify({
        "token": encoded_token,
        "expires_in": 3600,
        "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
    })
```

**Запрос:**
```bash
curl http://localhost:5000/generate_datalens_token
```

**Ответ:**
```json
{
  "token": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "generated_at": "2025-10-19 12:30:45"
}
```

---

## 🖥️ Встраивание дашборда

### HTML код

```html
<!DOCTYPE html>
<html>
<head>
    <title>Аэрометр - Дашборд</title>
</head>
<body>
    <h1>Статистика полетов БПЛА</h1>
    
    <!-- Встраиваемый дашборд DataLens -->
    <iframe 
        src="https://datalens.yandex.ru/embed/8e0tatm9jpjit?_embedded=1&_theme=light&_lang=ru&_no_controls=1"
        width="100%" 
        height="800px" 
        frameborder="0"
        id="datalens-iframe">
    </iframe>
    
    <script>
        // Получение JWT токена
        async function loadDashboard() {
            const response = await fetch('/generate_datalens_token');
            const data = await response.json();
            
            // Добавление токена в URL iframe
            const iframe = document.getElementById('datalens-iframe');
            const baseUrl = iframe.src.split('?')[0];
            iframe.src = `${baseUrl}?_token=${data.token}&_embedded=1&_theme=light&_lang=ru`;
        }
        
        // Загрузка при открытии страницы
        loadDashboard();
        
        // Обновление токена каждые 50 минут
        setInterval(loadDashboard, 50 * 60 * 1000);
    </script>
</body>
</html>
```

### Параметры встраивания

| Параметр | Описание | Значения |
|----------|----------|----------|
| `_embedded=1` | Режим встраивания | 0, 1 |
| `_theme` | Тема оформления | light, dark |
| `_lang` | Язык интерфейса | ru, en |
| `_no_controls=1` | Скрыть элементы управления | 0, 1 |
| `_token` | JWT токен аутентификации | строка |

---

## 📊 Структура дашбордов

### Основные дашборды

#### 1. Главный дашборд
- **Общая статистика** по России
- **Карта интенсивности** полетов
- **Топ-10 регионов** по количеству полетов
- **Динамика по месяцам**
- **Распределение по времени суток**

#### 2. Региональная аналитика
- **Выбор региона** (фильтр)
- **Статистика по региону**
- **Сравнение с другими регионами**
- **Тренды и прогнозы**

#### 3. Площадки БПЛА
- **Карта 290 площадок**
- **Рейтинг площадок**
- **Трафик в зонах**
- **Запретные зоны**

#### 4. Real-time мониторинг
- **Активные самолеты** (последний час)
- **Карта полетов** в реальном времени
- **Статус обработки** файлов
- **Системные метрики**

---

## 🎨 Типы чартов

### Карты

```
- Тепловая карта плотности полетов
- Точечная карта самолетов
- Полигональная карта регионов
- Гексагональная сетка H3
```

### Графики

```
- Линейные графики динамики
- Столбчатые диаграммы сравнения
- Круговые диаграммы распределения
- Воронки конверсии
```

### Таблицы

```
- Сводные таблицы статистики
- Детализация по регионам
- Топ-N элементов
- Drill-down таблицы
```

---

## 📥 Экспорт/Импорт конфигурации

### Экспорт дашборда

**Через UI DataLens:**
1. Откройте дашборд в DataLens
2. Меню → Экспорт
3. Выберите формат JSON
4. Сохраните файл

**Через API:**
```bash
curl -X GET \
  -H "Authorization: Bearer <YC_TOKEN>" \
  "https://datalens.yandex.ru/api/v1/dashboards/<DASHBOARD_ID>/export"
```

### Импорт конфигурации

**Через UI DataLens:**
1. DataLens → Создать → Импортировать
2. Выберите файл `lct.json`
3. Нажмите "Импортировать"

**Через CLI:**
```bash
# Установка YC CLI
curl https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Аутентификация
yc init

# Импорт
yc datalens dashboard import --file Datalens/lct.json
```

---

## 🔧 Конфигурация

### Настройки в settings.py

```python
# RSA приватный ключ для JWT
private_key = b"""-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAxIRIjBo/YIVee+R8xUEDGH0MdBsnMxnjbNvHL3C+EqhsHNsi
...
-----END RSA PRIVATE KEY-----"""

# ID встраиваемого дашборда
DATALENS_EMBED_ID = "8e0tatm9jpjit"

# Время жизни токена (секунды)
DATALENS_TOKEN_TTL = 3600  # 1 час
```

### Генерация RSA ключей

```bash
# Генерация приватного ключа
openssl genrsa -out private_key.pem 2048

# Извлечение публичного ключа
openssl rsa -in private_key.pem -pubout -out public_key.pem

# Просмотр ключа
cat private_key.pem
```

**Важно:** Публичный ключ нужно зарегистрировать в настройках DataLens!

---

## 🗃️ Подключение к базе данных

### Настройка в DataLens

1. **Создание подключения**
   - Тип: MySQL
   - Хост: `31.31.197.64`
   - Порт: `3306`
   - База: `u3253297_hack`
   - Пользователь: `u3253297_hack`
   - SSL: Опционально

2. **Создание датасета**
   - Выбор таблиц: `processed_flights`, `regions`, `region_stats`, etc.
   - Настройка связей между таблицами
   - Определение полей и их типов

3. **Создание чартов**
   - Выбор типа визуализации
   - Настройка осей и мер
   - Применение фильтров

---

## 📊 SQL-запросы для DataLens

### Примеры датасетов

#### Статистика по регионам

```sql
SELECT 
    r.name as region_name,
    rs.date,
    rs.total_flights,
    rs.peak_load,
    rs.flight_density,
    rs.morning_flights,
    rs.afternoon_flights,
    rs.evening_flights,
    rs.night_flights
FROM region_stats rs
JOIN regions r ON rs.region_id = r.id
WHERE rs.prediction = 'download'
```

#### Топ регионов по трафику

```sql
SELECT 
    region,
    SUM(total_flights) as total,
    AVG(flight_density) as avg_density,
    MAX(peak_load) as max_peak
FROM region_stats
WHERE prediction = 'download'
GROUP BY region
ORDER BY total DESC
LIMIT 10
```

#### Активные самолеты

```sql
SELECT 
    a.icao24,
    a.callsign,
    a.latitude,
    a.longitude,
    a.baro_altitude,
    a.velocity,
    r.name as region
FROM aircraft a
LEFT JOIN regions r ON a.region_id = r.id
WHERE a.last_updated >= NOW() - INTERVAL 1 HOUR
```

---

## 🎨 Кастомизация

### Цветовые схемы

**Для тепловой карты:**
```
Низкая плотность: #00FF00 (зеленый)
Средняя плотность: #FFFF00 (желтый)
Высокая плотность: #FF8800 (оранжевый)
Очень высокая: #FF0000 (красный)
```

**Для статусов:**
```
Активный: #4cc9f0 (голубой)
Обработка: #ffc300 (желтый)
Ошибка: #e63946 (красный)
Успех: #06d6a0 (зеленый)
```

### Форматирование

```javascript
// Числа
{
  "format": {
    "type": "number",
    "precision": 2,
    "thousand_separator": " ",
    "decimal_separator": ","
  }
}

// Проценты
{
  "format": {
    "type": "percent",
    "precision": 1
  }
}

// Даты
{
  "format": {
    "type": "date",
    "format": "DD.MM.YYYY"
  }
}
```

---

## 🔍 Фильтры и параметры

### Глобальные фильтры

**Период:**
```sql
date BETWEEN :date_from AND :date_to
```

**Регион:**
```sql
region_id = :region_id
```

**Тип данных:**
```sql
prediction IN (:prediction_types)
```

### Динамические параметры

```javascript
// Передача параметров через URL
const url = `https://datalens.yandex.ru/embed/${embedId}?` + 
  `region_id=77&` +
  `date_from=2024-01-01&` +
  `date_to=2025-12-31&` +
  `_token=${jwt_token}`;
```

---

## 📈 Производительность

### Оптимизация запросов

1. **Индексы** на часто используемых полях
2. **Агрегация** на уровне БД
3. **Кеширование** результатов
4. **Партиционирование** больших таблиц

### Кеширование в DataLens

```
- Время жизни кеша: 5-60 минут
- Автоматическое обновление
- Ручная очистка кеша
```

---

## 🛠️ Troubleshooting

### Проблема: Токен не работает

**Решения:**
1. Проверьте время на сервере (синхронизация NTP)
2. Убедитесь, что публичный ключ зарегистрирован в DataLens
3. Проверьте формат ключа (PEM, PKCS#1)
4. Проверьте `embedId` — он должен совпадать

### Проблема: Дашборд не загружается

**Решения:**
1. Проверьте CORS настройки
2. Убедитесь, что iframe не заблокирован
3. Проверьте консоль браузера на ошибки
4. Проверьте подключение к БД

### Проблема: Устаревшие данные

**Решения:**
1. Очистите кеш DataLens
2. Проверьте время обновления датасета
3. Принудительно обновите данные в БД

---

## 📝 Best Practices

1. **Регулярное обновление токенов** (каждые 50 минут)
2. **Мониторинг производительности** запросов
3. **Версионирование** конфигурации (`lct.json`)
4. **Резервное копирование** дашбордов
5. **Документирование** изменений
6. **Тестирование** на тестовом окружении

---

## 🔗 Полезные ссылки

### Документация

- **DataLens**: https://cloud.yandex.ru/docs/datalens/
- **JWT**: https://jwt.io/
- **PyJWT**: https://pyjwt.readthedocs.io/

### Инструменты

- **JWT Debugger**: https://jwt.io/#debugger
- **DataLens Gallery**: https://datalens.yandex.ru/gallery
- **API Reference**: https://cloud.yandex.ru/docs/datalens/api-ref/

---

## 📄 Лицензия

Проприетарное программное обеспечение. Все права защищены © 2025 Команда Finance.

---

**Дата:** 19 октября 2025  
**Версия документации:** 1.0.0  
**Модуль:** DataLens Integration
