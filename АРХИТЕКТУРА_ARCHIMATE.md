# 🏛️ Архитектура АЭРОМЕТР в нотации ArchiMate

**Версия:** 2.0.0  
**Дата:** 19 октября 2025  
**Проект:** АЭРОМЕТР  
**Стандарт:** ArchiMate 3.1

---

## 📋 Содержание

- [1. Введение](#1-введение)
- [2. Motivation Layer — Слой мотивации](#2-motivation-layer--слой-мотивации)
- [3. Strategy Layer — Стратегический слой](#3-strategy-layer--стратегический-слой)
- [4. Business Layer — Бизнес-слой](#4-business-layer--бизнес-слой)
- [5. Application Layer — Слой приложений](#5-application-layer--слой-приложений)
- [6. Technology Layer — Технологический слой](#6-technology-layer--технологический-слой)
- [7. Implementation & Migration Layer](#7-implementation--migration-layer)
- [8. Viewpoints — Точки зрения](#8-viewpoints--точки-зрения)

---

## 1. Введение

Данный документ описывает архитектуру системы **АЭРОМЕТР** с использованием нотации ArchiMate 3.1. ArchiMate — это открытый независимый язык моделирования архитектуры предприятия, который обеспечивает единообразные инструменты для описания, анализа и визуализации архитектуры.

### 1.1 Цель документа

Предоставить комплексное описание архитектуры системы АЭРОМЕТР на всех уровнях абстракции: от бизнес-целей до технической инфраструктуры.

### 1.2 Область применения

- Enterprise Architects
- Solution Architects
- IT Managers
- Development Teams
- Stakeholders

---

## 2. Motivation Layer — Слой мотивации

### 2.1 Stakeholders (Заинтересованные стороны)

| ID | Stakeholder | Описание |
|----|------------|----------|
| STK-001 | **Росавиация** | Федеральное агентство воздушного транспорта |
| STK-002 | **Минтранс РФ** | Министерство транспорта РФ |
| STK-003 | **Операторы БПЛА** | Компании и физические лица, выполняющие полеты |
| STK-004 | **Региональные власти** | Администрации субъектов РФ |
| STK-005 | **Аналитики** | Специалисты по обработке данных |
| STK-006 | **IT-департамент** | Техническая поддержка и развитие |

### 2.2 Drivers (Драйверы)

| ID | Driver | Описание |
|----|--------|----------|
| DRV-001 | **Национальный проект БАС** | Национальный проект "Беспилотные авиационные системы" (2024-2030) |
| DRV-002 | **Цифровизация авиации** | Переход на цифровые технологии в авиационной отрасли |
| DRV-003 | **Рост рынка БПЛА** | Экспоненциальный рост использования беспилотников |
| DRV-004 | **Безопасность полетов** | Необходимость контроля за воздушным пространством |
| DRV-005 | **Оптимизация инфраструктуры** | Размещение 290 посадочных площадок к 2030 году |

### 2.3 Assessment (Оценка)

| ID | Assessment | Значение | Описание |
|----|-----------|----------|----------|
| ASM-001 | **Ручная обработка данных** | Негативно | Высокие трудозатраты госучреждений |
| ASM-002 | **Отсутствие единой системы** | Негативно | Разрозненные источники данных |
| ASM-003 | **Растущий объем данных** | Проблема | Невозможность обработки вручную |
| ASM-004 | **Спрос на аналитику** | Позитивно | Запрос на данные от регионов |

### 2.4 Goals (Цели)

| ID | Goal | Описание |
|----|------|----------|
| GOL-001 | **Автоматизация сбора данных** | Автоматический парсинг файлов с FTP и внешних API |
| GOL-002 | **Единая база данных полетов** | Централизованное хранилище данных о полетах БПЛА |
| GOL-003 | **Аналитика в реальном времени** | Предоставление актуальной статистики и дашбордов |
| GOL-004 | **Оптимальное размещение площадок** | Расчет оптимальных мест для 290 площадок |
| GOL-005 | **Прогнозирование полетов** | Предсказание полетной активности по регионам |
| GOL-006 | **Снижение трудозатрат** | Сокращение времени на формирование отчетов на 90% |

### 2.5 Outcomes (Результаты)

| ID | Outcome | Описание |
|----|---------|----------|
| OUT-001 | **Экономия времени** | Сокращение времени обработки данных с недель до минут |
| OUT-002 | **Повышение качества данных** | Автоматическая валидация и устранение ошибок |
| OUT-003 | **Информированные решения** | Принятие решений на основе данных |
| OUT-004 | **Прозрачность статистики** | Открытый доступ к агрегированным данным |

### 2.6 Principles (Принципы)

| ID | Principle | Описание |
|----|-----------|----------|
| PRC-001 | **Автоматизация** | Максимальная автоматизация процессов |
| PRC-002 | **Модульность** | Слабая связанность компонентов |
| PRC-003 | **Масштабируемость** | Возможность роста нагрузки |
| PRC-004 | **Открытость** | Использование открытых стандартов и API |
| PRC-005 | **Безопасность** | Защита персональных данных |
| PRC-006 | **Надежность** | Отказоустойчивость и резервирование |

### 2.7 Requirements (Требования)

| ID | Requirement | Приоритет | Описание |
|----|-------------|-----------|----------|
| REQ-001 | **Парсинг Excel файлов** | Критичный | Обработка стандартизированных сообщений Росавиации |
| REQ-002 | **Геопривязка к регионам** | Критичный | Точная привязка координат к субъектам РФ |
| REQ-003 | **REST API** | Высокий | Интерфейс для интеграции с внешними системами |
| REQ-004 | **BI-дашборды** | Высокий | Визуализация данных для аналитиков |
| REQ-005 | **Real-time мониторинг** | Средний | Отслеживание воздушных судов |
| REQ-006 | **Мобильная адаптация** | Низкий | Доступ с мобильных устройств |

---

## 3. Strategy Layer — Стратегический слой

### 3.1 Resources (Ресурсы)

| ID | Resource | Тип | Описание |
|----|----------|-----|----------|
| RES-001 | **Финансирование НП БАС** | Финансы | 696 млрд рублей (2024-2030) |
| RES-002 | **Команда разработки** | Человеческие | Team Finance (разработчики, аналитики) |
| RES-003 | **Серверная инфраструктура** | Технические | Облачные сервера |
| RES-004 | **Данные Росавиации** | Информационные | Excel файлы на FTP |
| RES-005 | **Open Data** | Информационные | OpenSky, Росреестр, SkyArc |

### 3.2 Capabilities (Возможности)

| ID | Capability | Уровень | Описание |
|----|-----------|---------|----------|
| CAP-001 | **Обработка больших данных** | 4/5 | 50,000 записей/минуту |
| CAP-002 | **Геопространственный анализ** | 5/5 | H3, Shapely, R-Tree |
| CAP-003 | **Machine Learning** | 3/5 | Базовое прогнозирование |
| CAP-004 | **API разработка** | 4/5 | Flask REST API |
| CAP-005 | **Web-разработка** | 4/5 | PHP, JavaScript |
| CAP-006 | **DevOps** | 3/5 | CI/CD базовый уровень |

### 3.3 Courses of Action (Направления действий)

| ID | Course of Action | Период | Описание |
|----|------------------|--------|----------|
| COA-001 | **Разработка MVP** | Месяц 1-3 | Базовый функционал парсинга и визуализации |
| COA-002 | **Интеграция с внешними API** | Месяц 2-4 | OpenSky, SkyArc, OSM |
| COA-003 | **Развитие аналитики** | Месяц 4-6 | Прогнозирование, ML-модели |
| COA-004 | **Масштабирование** | Месяц 6-12 | Оптимизация производительности |

---

## 4. Business Layer — Бизнес-слой

### 4.1 Business Actors (Бизнес-акторы)

| ID | Actor | Роль | Описание |
|----|-------|------|----------|
| BAC-001 | **Оператор БПЛА** | Внешний | Подает заявки на полеты |
| BAC-002 | **Аналитик Росавиации** | Пользователь | Анализирует статистику полетов |
| BAC-003 | **Региональный чиновник** | Пользователь | Получает отчеты по региону |
| BAC-004 | **Администратор системы** | Внутренний | Управляет системой |
| BAC-005 | **Разработчик** | Внутренний | Развивает систему |

### 4.2 Business Roles (Бизнес-роли)

| ID | Role | Ответственность |
|----|------|-----------------|
| BRL-001 | **Data Provider** | Предоставление данных о полетах |
| BRL-002 | **Data Consumer** | Потребление аналитики и отчетов |
| BRL-003 | **System Administrator** | Управление конфигурацией и пользователями |
| BRL-004 | **Business Analyst** | Анализ требований и KPI |

### 4.3 Business Processes (Бизнес-процессы)

#### BP-001: Обработка данных о полетах

```
Входы: Excel файл с FTP
Выходы: Записи в БД, статистика

Шаги:
1. Загрузка файла с FTP
2. Парсинг Excel
3. Валидация данных
4. Геопривязка к регионам
5. Сохранение в БД
6. Обновление статистики
7. Генерация отчетов
```

#### BP-002: Анализ полетной активности

```
Входы: Данные из БД
Выходы: Дашборды, отчеты

Шаги:
1. Выборка данных по фильтрам
2. Агрегация статистики
3. Расчет метрик
4. Генерация визуализаций
5. Публикация дашбордов
```

#### BP-003: Планирование размещения площадок

```
Входы: История полетов, запретные зоны
Выходы: Список 290 площадок

Шаги:
1. Анализ трафика по гексагонам
2. Учет запретных зон
3. Расчет рейтингов
4. Оптимизация размещения
5. Распределение по годам
6. Сохранение результатов
```

#### BP-004: Мониторинг в реальном времени

```
Входы: OpenSky Network API
Выходы: Актуальные данные о воздушных судах

Шаги:
1. Запрос данных из OpenSky
2. Фильтрация по территории РФ
3. Геопривязка к регионам
4. Обновление БД
5. Отображение на карте
6. Автоочистка устаревших данных
```

### 4.4 Business Functions (Бизнес-функции)

| ID | Function | Описание |
|----|----------|----------|
| BFN-001 | **Сбор данных** | Автоматическая загрузка из источников |
| BFN-002 | **Обработка данных** | Парсинг, валидация, нормализация |
| BFN-003 | **Хранение данных** | Централизованная БД |
| BFN-004 | **Анализ данных** | Расчет метрик и статистики |
| BFN-005 | **Визуализация** | Дашборды и отчеты |
| BFN-006 | **Прогнозирование** | Предсказание трендов |

### 4.5 Business Services (Бизнес-сервисы)

| ID | Service | Потребители | Описание |
|----|---------|-------------|----------|
| BSV-001 | **Региональная аналитика** | Региональные власти | Статистика полетов по региону |
| BSV-002 | **Национальная аналитика** | Росавиация, Минтранс | Статистика по всей РФ |
| BSV-003 | **Планирование инфраструктуры** | НП БАС | Оптимальные места площадок |
| BSV-004 | **Открытые данные** | Граждане, исследователи | API для доступа к данным |
| BSV-005 | **Мониторинг воздушного пространства** | Авиадиспетчеры | Real-time трекинг |

### 4.6 Business Objects (Бизнес-объекты)

| ID | Object | Атрибуты | Описание |
|----|--------|----------|----------|
| BOB-001 | **Полет БПЛА** | ID, дата, время, координаты, длительность, оператор | Запись о полете |
| BOB-002 | **Регион РФ** | ID, название, полигон, площадь, население | Субъект федерации |
| BOB-003 | **Площадка БПЛА** | ID, координаты, рейтинг, год ввода | Посадочная площадка |
| BOB-004 | **Воздушное судно** | ICAO24, позывной, координаты, высота, скорость | Самолет/БПЛА в небе |
| BOB-005 | **Статистика региона** | Регион, период, полетов, плотность | Агрегированные данные |
| BOB-006 | **Запретная зона** | ID, полигон, тип, активность | Зона ограничения полетов |

---

## 5. Application Layer — Слой приложений

### 5.1 Application Components (Компоненты приложений)

#### Frontend Layer

| ID | Component | Технология | Назначение |
|----|-----------|-----------|------------|
| APC-001 | **Web UI** | PHP 7.4+, HTML5, CSS3, JS | Пользовательский интерфейс |
| APC-002 | **Map Viewer** | Yandex Maps API | Картографический интерфейс |
| APC-003 | **Dashboard UI** | Yandex DataLens | BI-дашборды |
| APC-004 | **Report Generator** | TCPDF, HTML2Canvas | Генерация PDF отчетов |

#### Backend Layer

| ID | Component | Технология | Назначение |
|----|-----------|-----------|------------|
| APC-010 | **Parser Module** | Python 3.8+ | Парсинг Excel файлов |
| APC-011 | **Aircraft Module** | Python 3.8+ | Сбор данных OpenSky |
| APC-012 | **Grid Generator** | Python 3.8+, H3 | Генерация сеток |
| APC-013 | **Area BPLA Generator** | Python 3.8+ | Размещение площадок |
| APC-014 | **Prediction Module** | Python 3.8+ | Прогнозирование |
| APC-015 | **Rosreestr Module** | Python 3.8+ | Загрузка официальных границ Росреестра |
| APC-016 | **Image Generator** | FusionBrain, GigaChat | Генерация изображений |
| APC-017 | **REST API** | Flask 2.0+ | API для интеграции |
| APC-018 | **Background Scheduler** | Schedule | Фоновые задачи |

### 5.2 Application Functions (Функции приложений)

| ID | Function | Реализация | Описание |
|----|----------|------------|----------|
| AFN-001 | **FTP Client** | ftplib (Python) | Загрузка файлов |
| AFN-002 | **Excel Parser** | openpyxl (Python) | Чтение Excel |
| AFN-003 | **Coordinate Parser** | Regex, Shapely | Парсинг координат |
| AFN-004 | **Geo-matcher** | R-Tree, Shapely, Fiona, GeoPandas | Геопривязка к регионам Росреестра (без буферов) |
| AFN-005 | **Statistics Calculator** | Pandas, NumPy | Расчет метрик |
| AFN-006 | **Data Validator** | Custom validators | Валидация данных |
| AFN-007 | **H3 Indexer** | h3-py | Гексагональная индексация |
| AFN-008 | **HTTP Client** | Requests | Запросы к внешним API |
| AFN-009 | **JSON/GeoJSON Parser** | json, osm2geojson | Парсинг геоданных |
| AFN-010 | **JWT Generator** | PyJWT | Генерация токенов |

### 5.3 Application Interfaces (Интерфейсы приложений)

| ID | Interface | Тип | Протокол | Описание |
|----|-----------|-----|----------|----------|
| AIN-001 | **REST API** | Synchronous | HTTP/HTTPS | JSON REST API |
| AIN-002 | **Web UI** | User Interface | HTTP/HTTPS | Веб-интерфейс |
| AIN-003 | **FTP Interface** | File Transfer | FTP | Загрузка Excel |
| AIN-004 | **OpenSky API** | External | HTTP/REST | Данные о судах |
| AIN-005 | **Rosreestr SHP** | File | SHP/XML | Официальные границы РФ |
| AIN-006 | **SkyArc API** | External | HTTP/REST | Запретные зоны |
| AIN-007 | **FusionBrain API** | External | HTTP/REST | Генерация изображений |
| AIN-008 | **DataLens Embed** | Embedded | HTTPS/JWT | Встраивание дашбордов |
| AIN-009 | **Database API** | Internal | MySQL Protocol | Доступ к БД |

### 5.4 Application Services (Сервисы приложений)

| ID | Service | Endpoint | Описание |
|----|---------|----------|----------|
| ASV-001 | **Process Files** | POST /process_files | Обработка файлов |
| ASV-002 | **Update Region Stats** | POST /update_region_stats | Обновление статистики |
| ASV-003 | **Update Aircraft** | POST /update_aircraft_data | Обновление судов |
| ASV-004 | **Generate Grids** | POST /generate_grids | Генерация сеток |
| ASV-005 | **Generate Predictions** | POST /generate_predictions | Прогнозирование |
| ASV-006 | **Get Region Stats** | GET /region_stats | Получение статистики |
| ASV-007 | **Create Backup** | POST /create_backup | Создание бэкапа |
| ASV-008 | **Generate DataLens Token** | GET /generate_datalens_token | JWT токен |

### 5.5 Data Objects (Объекты данных)

| ID | Object | Schema | Описание |
|----|--------|--------|----------|
| ADO-001 | **Flight Record** | processed_flights | Запись о полете |
| ADO-002 | **Region** | regions | Регион РФ |
| ADO-003 | **Aircraft State** | aircraft | Воздушное судно |
| ADO-004 | **Hexagon** | grid_hexagon | H3 гексагон |
| ADO-005 | **Square Grid** | grid_square | Квадратная ячейка |
| ADO-006 | **BPLA Area** | area_bpla | Площадка БПЛА |
| ADO-007 | **Region Stats** | region_stats | Статистика региона |
| ADO-008 | **Forbidden Zone** | points | Запретная зона |

---

## 6. Technology Layer — Технологический слой

### 6.1 Nodes (Узлы)

| ID | Node | Тип | Характеристики | Назначение |
|----|------|-----|----------------|------------|
| NOD-001 | **Web Server** | Virtual | Apache/Nginx | Хостинг Frontend |
| NOD-002 | **Application Server** | Virtual | 4 CPU, 8GB RAM | Python Backend |
| NOD-003 | **Database Server** | Virtual | 4 CPU, 16GB RAM, SSD | MySQL 8.0 |
| NOD-004 | **FTP Server** | External | N/A | Источник файлов |
| NOD-005 | **User Workstation** | Physical | Browser | Клиентское устройство |

### 6.2 Devices (Устройства)

| ID | Device | Описание |
|----|--------|----------|
| DEV-001 | **Desktop PC** | Рабочая станция аналитика |
| DEV-002 | **Laptop** | Мобильная работа |
| DEV-003 | **Tablet** | Просмотр дашбордов |
| DEV-004 | **Smartphone** | Мобильный доступ |

### 6.3 System Software (Системное ПО)

| ID | Software | Версия | Назначение |
|----|----------|--------|------------|
| SYS-001 | **Linux** | CentOS 7+ / Ubuntu 20.04+ | Операционная система |
| SYS-002 | **Python** | 3.8+ | Runtime для Backend |
| SYS-003 | **PHP** | 7.4+ | Runtime для Frontend |
| SYS-004 | **MySQL** | 8.0+ | СУБД |
| SYS-005 | **Apache httpd** | 2.4+ | Web Server |
| SYS-006 | **mod_wsgi** | Latest | Python WSGI для Apache |

### 6.4 Technology Services (Технологические сервисы)

| ID | Service | Технология | Описание |
|----|---------|-----------|----------|
| TSV-001 | **Database Service** | MySQL 8.0 | Хранение данных |
| TSV-002 | **File Storage** | Linux FS | Локальное хранилище |
| TSV-003 | **HTTP Service** | Apache/Nginx | Веб-сервер |
| TSV-004 | **Python Runtime** | Python 3.8+ | Исполнение Python |
| TSV-005 | **PHP-FPM** | PHP 7.4+ | FastCGI для PHP |
| TSV-006 | **Cron/Systemd** | Linux | Планировщик задач |

### 6.5 Communication Paths (Пути коммуникации)

| ID | Path | Протокол | Порт | Описание |
|----|------|----------|------|----------|
| COM-001 | **Web Traffic** | HTTPS | 443 | Браузер ↔ Web Server |
| COM-002 | **API Calls** | HTTP/HTTPS | 5000 | Frontend ↔ Flask API |
| COM-003 | **Database Connections** | MySQL Protocol | 3306 | App ↔ MySQL |
| COM-004 | **FTP Download** | FTP | 21 | Backend ↔ FTP Server |
| COM-005 | **External API** | HTTPS | 443 | Backend ↔ External APIs |

### 6.6 Technology Interfaces (Технологические интерфейсы)

| ID | Interface | Стандарт | Описание |
|----|-----------|----------|----------|
| TIN-001 | **MySQL Connector** | MySQL Protocol | Python ↔ MySQL |
| TIN-002 | **WSGI** | PEP 3333 | Flask ↔ Web Server |
| TIN-003 | **FastCGI** | RFC 3875 | PHP ↔ Web Server |
| TIN-004 | **REST over HTTP** | HTTP/1.1, JSON | API communication |
| TIN-005 | **FTP Client** | RFC 959 | File transfer |

### 6.7 Artifacts (Артефакты)

| ID | Artifact | Формат | Описание |
|----|----------|--------|----------|
| ART-001 | **Excel Files** | .xlsx | Исходные данные |
| ART-002 | **Python Scripts** | .py | Исходный код Backend |
| ART-003 | **PHP Scripts** | .php | Исходный код Frontend |
| ART-004 | **SQL Dump** | .sql | Дамп базы данных |
| ART-005 | **Configuration Files** | .py, .php, .conf | Конфигурация |
| ART-006 | **Docker Images** | Docker | Контейнеры (future) |
| ART-007 | **Log Files** | .log | Журналы системы |
| ART-008 | **PDF Reports** | .pdf | Отчеты |

---

## 7. Implementation & Migration Layer

### 7.1 Work Packages (Рабочие пакеты)

| ID | Work Package | Длительность | Описание |
|----|--------------|--------------|----------|
| WPK-001 | **Проектирование** | 2 недели | Дизайн архитектуры и БД |
| WPK-002 | **Backend Core** | 4 недели | Разработка модулей парсинга |
| WPK-003 | **Frontend Development** | 4 недели | Веб-интерфейс |
| WPK-004 | **API Integration** | 3 недели | Интеграция внешних API |
| WPK-005 | **BI Dashboards** | 2 недели | DataLens дашборды |
| WPK-006 | **Testing** | 2 недели | Тестирование системы |
| WPK-007 | **Deployment** | 1 неделя | Развертывание в прод |
| WPK-008 | **Documentation** | 1 неделя | Техническая документация |

### 7.2 Deliverables (Поставляемые результаты)

| ID | Deliverable | Тип | Описание |
|----|-------------|-----|----------|
| DEL-001 | **Архитектурная документация** | Документ | ArchiMate модели |
| DEL-002 | **Рабочая система** | ПО | АЭРОМЕТР v2.0 |
| DEL-003 | **База данных** | Данные | Заполненная БД |
| DEL-004 | **API документация** | Документ | REST API спецификация |
| DEL-005 | **Руководство пользователя** | Документ | User manual |
| DEL-006 | **Руководство администратора** | Документ | Admin guide |

### 7.3 Implementation Events (События внедрения)

| ID | Event | Дата | Описание |
|----|-------|------|----------|
| EVT-001 | **Kick-off** | T+0 недель | Старт проекта |
| EVT-002 | **Architecture Review** | T+2 недели | Ревью архитектуры |
| EVT-003 | **MVP Demo** | T+6 недель | Демонстрация MVP |
| EVT-004 | **Alpha Release** | T+10 недель | Альфа-версия |
| EVT-005 | **Beta Release** | T+12 недель | Бета-версия |
| EVT-006 | **Go-Live** | T+14 недель | Запуск в продакшн |
| EVT-007 | **Post-Launch Review** | T+16 недель | Ретроспектива |

### 7.4 Plateaus (Плато)

| ID | Plateau | Дата достижения | Характеристики |
|----|---------|----------------|----------------|
| PLT-001 | **Baseline** | T+0 | Ручная обработка данных |
| PLT-002 | **MVP** | T+6 недель | Базовый парсинг и визуализация |
| PLT-003 | **v1.0** | T+12 недель | Полный функционал без внешних API |
| PLT-004 | **v2.0** | T+14 недель | Интеграция с OpenSky, H3, прогнозы |
| PLT-005 | **v3.0** | T+6 месяцев | ML-модели, автомасштабирование |

### 7.5 Gaps (Разрывы)

| ID | Gap | Приоритет | Решение |
|----|-----|-----------|---------|
| GAP-001 | **Отсутствие аутентификации** | Высокий | Внедрение OpenID Connect |
| GAP-002 | **Нет мобильного приложения** | Средний | Разработка native apps |
| GAP-003 | **Ручное резервное копирование** | Средний | Автоматизация бэкапов |
| GAP-004 | **Один сервер** | Высокий | Репликация и балансировка |
| GAP-005 | **Базовые ML-модели** | Низкий | Улучшение алгоритмов |

---

## 8. Viewpoints — Точки зрения

### 8.1 Stakeholder Viewpoint (Точка зрения заинтересованных сторон)

**Цель:** Показать ценность системы для каждой группы stakeholders

**Заинтересованные стороны:**
- **Росавиация**: Автоматизация отчетности, снижение трудозатрат
- **Региональные власти**: Доступ к статистике по региону
- **Операторы БПЛА**: Прозрачность процессов
- **IT-департамент**: Современная архитектура, документация

**Проблемы, решаемые системой:**
1. Ручная обработка данных → Автоматический парсинг
2. Разрозненные источники → Единая БД
3. Долгие отчеты → Мгновенные дашборды
4. Нет аналитики → Прогнозы и метрики

### 8.2 Business Process Cooperation Viewpoint

**Главные процессы:**

```
[Оператор БПЛА] 
    ↓ Подает заявку
[FTP Сервер] 
    ↓ Файл .xlsx
[Парсинг] → [Валидация] → [Геопривязка] → [Сохранение в БД]
    ↓
[Расчет статистики] → [Обновление дашбордов]
    ↓
[Аналитик] просматривает статистику
```

### 8.3 Application Cooperation Viewpoint

**Взаимодействие приложений:**

```
[Web Browser]
    ↓ HTTPS
[PHP Frontend] ← → [Flask Backend]
    ↓                   ↓
[DataLens]         [MySQL DB]
                       ↑
                [External APIs]
                - OpenSky
                - OSM
                - SkyArc
```

### 8.4 Technology Usage Viewpoint

**Технологический стек:**

```
Presentation Tier:
- HTML5, CSS3, JavaScript
- Yandex Maps API
- DataLens

Application Tier:
- Python 3.8+ (Backend)
- PHP 7.4+ (Frontend)
- Flask (REST API)

Data Tier:
- MySQL 8.0
- File Storage (FTP)

Infrastructure:
- Linux (CentOS/Ubuntu)
- Apache/Nginx
- Docker (future)
```

### 8.5 Information Structure Viewpoint

**Основные информационные сущности:**

```
Flight (Полет)
├── ID
├── Date/Time
├── Coordinates (start, end)
├── Duration
├── Aircraft Type
├── Operator
└── Region → references Region

Region (Регион)
├── ID
├── Name
├── Polygon (geometry)
├── Area (km²)
└── Statistics → references RegionStats

Hexagon (Гексагон H3)
├── ID
├── H3 Index
├── Center (lat, lon)
├── Polygon
├── Flight Count
└── Region → references Region

BPLAArea (Площадка)
├── ID
├── Coordinates
├── Rating
├── Year (2026-2030)
└── Hexagon → references Hexagon
```

### 8.6 Service Realization Viewpoint

**Реализация сервиса "Региональная аналитика":**

```
Business Service: Региональная аналитика
    ↓ realized by
Application Service: GET /region_stats
    ↓ realized by
Application Component: REST API (Flask)
    ↓ uses
Data Object: region_stats
    ↓ stored in
Technology Service: MySQL Database
    ↓ runs on
Node: Database Server
```

### 8.7 Layered Viewpoint

**Слоистая архитектура:**

```
┌────────────────────────────────────────────┐
│          BUSINESS LAYER                     │
│  Процессы, Функции, Сервисы, Объекты      │
└────────────────────────────────────────────┘
                   ↕
┌────────────────────────────────────────────┐
│        APPLICATION LAYER                    │
│  Components, Services, Interfaces, Data    │
└────────────────────────────────────────────┘
                   ↕
┌────────────────────────────────────────────┐
│        TECHNOLOGY LAYER                     │
│  Nodes, Software, Networks, Artifacts      │
└────────────────────────────────────────────┘
```

### 8.8 Physical Viewpoint

**Физическое развертывание:**

```
Internet Cloud
    │
    ├─ [External APIs]
    │   ├─ OpenSky Network
    │   ├─ OpenStreetMap
    │   ├─ SkyArc
    │   └─ FusionBrain
    │
    ├─ [Production Environment]
    │   ├─ Web Server (Apache/Nginx)
    │   │   ├─ PHP Frontend
    │   │   └─ Static Assets
    │   │
    │   ├─ Application Server
    │   │   ├─ Flask API (:5000)
    │   │   ├─ Background Workers
    │   │   └─ Python Modules
    │   │
    │   └─ Database Server
    │       └─ MySQL 8.0 (:3306)
    │
    └─ [User Devices]
        ├─ Desktop Browsers
        ├─ Laptops
        └─ Mobile Devices
```

---

## 9. Relationships Matrix (Матрица связей)

### 9.1 Motivation ↔ Business

| Motivation | Business Element | Relationship |
|-----------|------------------|--------------|
| GOL-001 (Автоматизация) | BP-001 (Обработка данных) | realizes |
| GOL-002 (Единая БД) | BOB-001 (Полет БПЛА) | realizes |
| GOL-003 (Аналитика RT) | BSV-001 (Региональная аналитика) | realizes |
| GOL-004 (Размещение площадок) | BP-003 (Планирование размещения) | realizes |
| REQ-001 (Парсинг Excel) | BFN-002 (Обработка данных) | realizes |

### 9.2 Business ↔ Application

| Business | Application | Relationship |
|----------|-------------|--------------|
| BP-001 (Обработка данных) | APC-010 (Parser Module) | realized by |
| BP-003 (Планирование площадок) | APC-013 (Area BPLA Generator) | realized by |
| BP-004 (Мониторинг RT) | APC-011 (Aircraft Module) | realized by |
| BSV-001 (Региональная аналитика) | ASV-006 (Get Region Stats) | realized by |
| BOB-001 (Полет БПЛА) | ADO-001 (Flight Record) | realized by |

### 9.3 Application ↔ Technology

| Application | Technology | Relationship |
|-------------|-----------|--------------|
| APC-010 (Parser Module) | SYS-002 (Python 3.8+) | deployed on |
| APC-017 (REST API) | NOD-002 (Application Server) | deployed on |
| ADO-001 (Flight Record) | TSV-001 (Database Service) | stored in |
| APC-001 (Web UI) | NOD-001 (Web Server) | deployed on |
| AIN-009 (Database API) | COM-003 (DB Connections) | uses |

---

## 10. ArchiMate Model Exchange Format

### 10.1 Open Exchange File Format

Для импорта в Archi tool, можно использовать следующий XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<archimate:model 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:archimate="http://www.archimatetool.com/archimate"
    name="АЭРОМЕТР"
    id="aerometr-model"
    version="4.9.0">
  
  <folder name="Strategy" id="strategy-folder" type="strategy">
    <element 
        xsi:type="archimate:Resource"
        name="Финансирование НП БАС" 
        id="res-001"/>
    <element 
        xsi:type="archimate:Capability"
        name="Обработка больших данных" 
        id="cap-001"/>
  </folder>
  
  <folder name="Business" id="business-folder" type="business">
    <element 
        xsi:type="archimate:BusinessActor"
        name="Аналитик Росавиации" 
        id="bac-002"/>
    <element 
        xsi:type="archimate:BusinessProcess"
        name="Обработка данных о полетах" 
        id="bp-001"/>
    <element 
        xsi:type="archimate:BusinessService"
        name="Региональная аналитика" 
        id="bsv-001"/>
    <element 
        xsi:type="archimate:BusinessObject"
        name="Полет БПЛА" 
        id="bob-001"/>
  </folder>
  
  <folder name="Application" id="application-folder" type="application">
    <element 
        xsi:type="archimate:ApplicationComponent"
        name="Parser Module" 
        id="apc-010"/>
    <element 
        xsi:type="archimate:ApplicationComponent"
        name="REST API" 
        id="apc-017"/>
    <element 
        xsi:type="archimate:ApplicationService"
        name="Process Files" 
        id="asv-001"/>
    <element 
        xsi:type="archimate:DataObject"
        name="Flight Record" 
        id="ado-001"/>
  </folder>
  
  <folder name="Technology" id="technology-folder" type="technology">
    <element 
        xsi:type="archimate:Node"
        name="Application Server" 
        id="nod-002"/>
    <element 
        xsi:type="archimate:SystemSoftware"
        name="Python 3.8+" 
        id="sys-002"/>
    <element 
        xsi:type="archimate:SystemSoftware"
        name="MySQL 8.0" 
        id="sys-004"/>
    <element 
        xsi:type="archimate:TechnologyService"
        name="Database Service" 
        id="tsv-001"/>
  </folder>
  
  <folder name="Motivation" id="motivation-folder" type="motivation">
    <element 
        xsi:type="archimate:Stakeholder"
        name="Росавиация" 
        id="stk-001"/>
    <element 
        xsi:type="archimate:Driver"
        name="Национальный проект БАС" 
        id="drv-001"/>
    <element 
        xsi:type="archimate:Goal"
        name="Автоматизация сбора данных" 
        id="gol-001"/>
    <element 
        xsi:type="archimate:Requirement"
        name="Парсинг Excel файлов" 
        id="req-001"/>
  </folder>
  
  <!-- Relationships -->
  <folder name="Relations" id="relations-folder" type="relations">
    <element 
        xsi:type="archimate:RealizationRelationship"
        source="bp-001" 
        target="gol-001" 
        id="rel-001"/>
    <element 
        xsi:type="archimate:RealizationRelationship"
        source="apc-010" 
        target="bp-001" 
        id="rel-002"/>
    <element 
        xsi:type="archimate:AssignmentRelationship"
        source="sys-002" 
        target="apc-010" 
        id="rel-003"/>
  </folder>
  
</archimate:model>
```

### 10.2 CSV Export для Archi Import

Можно также создать CSV файлы для импорта в Archi:

**elements.csv:**
```csv
ID,Type,Name,Documentation
gol-001,Goal,Автоматизация сбора данных,Автоматический парсинг файлов с FTP и внешних API
bp-001,Business Process,Обработка данных о полетах,Полный цикл обработки от загрузки до сохранения
apc-010,Application Component,Parser Module,Модуль парсинга Excel файлов
sys-002,System Software,Python 3.8+,Runtime для Backend
```

**relations.csv:**
```csv
ID,Type,Source,Target,Name
rel-001,Realization,bp-001,gol-001,realizes
rel-002,Realization,apc-010,bp-001,realizes
rel-003,Assignment,sys-002,apc-010,runs on
```

---

## 11. Заключение

Данная архитектура в нотации ArchiMate описывает комплексную систему АЭРОМЕТР на всех уровнях:

1. **Motivation Layer** — Цели, требования, принципы
2. **Strategy Layer** — Ресурсы, возможности, направления
3. **Business Layer** — Процессы, функции, сервисы
4. **Application Layer** — Компоненты, интерфейсы, данные
5. **Technology Layer** — Инфраструктура, ПО, сети

### Ключевые преимущества архитектуры:

✅ **Модульность** — Слабая связанность компонентов  
✅ **Масштабируемость** — Возможность роста нагрузки  
✅ **Надежность** — Резервирование и автоочистка  
✅ **Открытость** — REST API и стандартные протоколы  
✅ **Автоматизация** — Фоновые процессы и планировщик  

### Дальнейшие шаги:

1. Импорт модели в Archi tool для визуализации
2. Создание детальных view (диаграмм) для каждого viewpoint
3. Согласование с stakeholders
4. Использование как основа для разработки

---

<div align="center">

**✈️ АЭРОМЕТР — ArchiMate Architecture Model**

Made with ❤️ by Team Finance

Версия 2.0.0 | 19 октября 2025

</div>

