# app.py
from flask import Flask, jsonify, render_template_string, request
import os
import threading
import time
import jwt
from parser.parser_file import FlightDataProcessor
from parser.region_stats_updater import update_region_stats_main
from aircraft.aircraft import Scheduler, DatabaseManager, AircraftDataProcessor
from aircraft.opensky_client import OpenSkyClient
from aircraft.polygon_processor import PolygonProcessor
from grid.grid_generator import GridGenerator
from prediction.prediction import FlightPredictorNew
from backup import BackupCreator
from settings import DB_CONFIG, private_key

app = Flask(__name__)

# Глобальные переменные для управления фоновыми процессами
background_threads = {}
background_threads_lock = threading.Lock()

# HTML шаблон для главной страницы с новым дизайном
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aerometr System - Панель управления</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #4361ee;
            --secondary: #3f37c9;
            --success: #4cc9f0;
            --info: #4895ef;
            --warning: #f72585;
            --danger: #e63946;
            --dark: #1e1e2d;
            --light: #f8f9fa;
            --sidebar-width: 260px;
            --header-height: 70px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            overflow-x: hidden;
        }

        .layout-wrapper {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Styles */
        .sidebar {
            width: var(--sidebar-width);
            background: linear-gradient(180deg, #1e1e2d 0%, #151521 100%);
            position: fixed;
            height: 100vh;
            left: 0;
            top: 0;
            z-index: 1000;
            border-right: 1px solid #2d2d3d;
            transition: all 0.3s ease;
        }

        .sidebar-header {
            padding: 25px 20px;
            border-bottom: 1px solid #2d2d3d;
            text-align: center;
        }

        .sidebar-header h2 {
            color: #fff;
            font-size: 1.4em;
            margin-bottom: 5px;
        }

        .sidebar-header p {
            color: #6c757d;
            font-size: 0.9em;
        }

        .sidebar-menu {
            padding: 20px 0;
        }

        .nav-item {
            margin-bottom: 5px;
        }

        .nav-link {
            display: flex;
            align-items: center;
            padding: 12px 20px;
            color: #9a9a9a;
            text-decoration: none;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }

        .nav-link:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.05);
            border-left-color: var(--primary);
        }

        .nav-link.active {
            color: #fff;
            background: rgba(67, 97, 238, 0.1);
            border-left-color: var(--primary);
        }

        .nav-link i {
            margin-right: 12px;
            width: 20px;
            text-align: center;
        }

        /* Main Content Styles */
        .main-content {
            flex: 1;
            margin-left: var(--sidebar-width);
            background: #0f0f23;
            min-height: 100vh;
        }

        .header {
            background: rgba(30, 30, 45, 0.8);
            backdrop-filter: blur(10px);
            padding: 0 30px;
            height: var(--header-height);
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #2d2d3d;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header h1 {
            color: #fff;
            font-size: 1.5em;
            font-weight: 600;
        }

        .content {
            padding: 30px;
        }

        /* Card Styles */
        .section-title {
            color: #fff;
            margin-bottom: 20px;
            font-size: 1.3em;
            font-weight: 600;
        }

        .methods-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .method-card {
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #2d2d3d;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .method-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--success));
        }

        .method-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border-color: var(--primary);
        }

        .method-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .method-icon {
            width: 50px;
            height: 50px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 1.3em;
            background: rgba(67, 97, 238, 0.1);
            color: var(--primary);
        }

        .method-name {
            font-size: 1.2em;
            font-weight: 600;
            color: #fff;
            flex: 1;
        }

        .method-endpoint {
            background: rgba(255, 255, 255, 0.05);
            padding: 12px 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            border: 1px solid #2d2d3d;
            color: #e0e0e0;
            word-break: break-all;
        }

        .method-method {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 10px;
            text-transform: uppercase;
        }

        .method-get {
            background: var(--success);
            color: #000;
        }

        .method-post {
            background: var(--primary);
            color: #fff;
        }

        .method-description {
            color: #9a9a9a;
            line-height: 1.5;
            margin-bottom: 20px;
            font-size: 0.95em;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            gap: 8px;
            font-size: 0.9em;
        }

        .btn-get {
            background: var(--success);
            color: #000;
        }

        .btn-get:hover {
            background: #3ab8d8;
            transform: translateY(-2px);
        }

        .btn-post {
            background: var(--primary);
            color: #fff;
        }

        .btn-post:hover {
            background: #3251d4;
            transform: translateY(-2px);
        }

        .btn-warning {
            background: var(--warning);
            color: #fff;
        }

        .btn-warning:hover {
            background: #e1156d;
            transform: translateY(-2px);
        }

        /* Status Section */
        .status-section {
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #2d2d3d;
            margin-top: 30px;
        }

        .status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .status-header h2 {
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .btn-refresh {
            background: #6c757d;
            color: white;
            padding: 8px 16px;
        }

        .btn-refresh:hover {
            background: #545b62;
        }

        .status-list {
            display: grid;
            gap: 10px;
        }

        .status-item {
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border-left: 4px solid var(--success);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .status-item.inactive {
            border-left-color: #6c757d;
        }

        .status-item.warning {
            border-left-color: var(--warning);
        }

        .status-name {
            font-weight: 600;
            color: #fff;
        }

        .status-details {
            color: #9a9a9a;
            font-size: 0.85em;
        }

        .no-processes {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #6c757d;
            font-size: 0.9em;
            padding: 20px;
            border-top: 1px solid #2d2d3d;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
            }

            .main-content {
                margin-left: 0;
            }

            .methods-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 1.2em;
            }
        }

        /* Loading animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Category badges */
        .category-badge {
            display: inline-block;
            padding: 4px 8px;
            background: rgba(67, 97, 238, 0.2);
            color: var(--primary);
            border-radius: 4px;
            font-size: 0.7em;
            font-weight: 600;
            margin-left: 10px;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <div class="layout-wrapper">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2>🚀 Aerometr System</h2>
                <p>Панель управления</p>
            </div>
            <div class="sidebar-menu">
                <div class="nav-item">
                    <a href="#data-processing" class="nav-link active">
                        <i class="fas fa-database"></i>
                        Обработка данных
                    </a>
                </div>
                <div class="nav-item">
                    <a href="#prediction" class="nav-link">
                        <i class="fas fa-chart-line"></i>
                        Предсказания
                    </a>
                </div>
                <div class="nav-item">
                    <a href="#utilities" class="nav-link">
                        <i class="fas fa-tools"></i>
                        Утилиты
                    </a>
                </div>
                <div class="nav-item">
                    <a href="#status" class="nav-link">
                        <i class="fas fa-heartbeat"></i>
                        Статус системы
                    </a>
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <div class="main-content">
            <header class="header">
                <h1>Панель управления Aerometr System</h1>
            </header>

            <div class="content">
                <!-- Data Processing Section -->
                <section id="data-processing">
                    <h2 class="section-title">
                        <i class="fas fa-database"></i>
                        Обработка данных
                    </h2>
                    <div class="methods-grid">
                        {% for method in methods_data_processing %}
                        <div class="method-card">
                            <div class="method-header">
                                <div class="method-icon">
                                    <i class="{{ method.icon }}"></i>
                                </div>
                                <div class="method-name">{{ method.name }}</div>
                            </div>
                            <div class="method-endpoint">
                                <span class="method-method method-{{ method.method.lower() }}">{{ method.method }}</span>
                                {{ method.endpoint }}
                            </div>
                            <div class="method-description">{{ method.description }}</div>
                            {% if method.method == 'POST' %}
                                <button class="btn btn-post" onclick="callEndpoint('{{ method.endpoint }}', 'POST', '{{ method.name }}')">
                                    <i class="fas fa-play"></i>Выполнить
                                </button>
                            {% else %}
                                <a class="btn btn-get" href="{{ method.endpoint }}" target="_blank">
                                    <i class="fas fa-external-link-alt"></i>Выполнить
                                </a>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                </section>

                <!-- Prediction Section -->
                <section id="prediction" style="margin-top: 50px;">
                    <h2 class="section-title">
                        <i class="fas fa-chart-line"></i>
                        Предсказания и аналитика
                    </h2>
                    <div class="methods-grid">
                        {% for method in methods_prediction %}
                        <div class="method-card">
                            <div class="method-header">
                                <div class="method-icon">
                                    <i class="{{ method.icon }}"></i>
                                </div>
                                <div class="method-name">{{ method.name }}</div>
                            </div>
                            <div class="method-endpoint">
                                <span class="method-method method-{{ method.method.lower() }}">{{ method.method }}</span>
                                {{ method.endpoint }}
                            </div>
                            <div class="method-description">{{ method.description }}</div>
                            {% if method.method == 'POST' %}
                                <button class="btn btn-post" onclick="callEndpoint('{{ method.endpoint }}', 'POST', '{{ method.name }}')">
                                    <i class="fas fa-play"></i>Выполнить
                                </button>
                            {% else %}
                                <a class="btn btn-get" href="{{ method.endpoint }}" target="_blank">
                                    <i class="fas fa-external-link-alt"></i>Выполнить
                                </a>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                </section>

                <!-- Utilities Section -->
                <section id="utilities" style="margin-top: 50px;">
                    <h2 class="section-title">
                        <i class="fas fa-tools"></i>
                        Утилиты и обслуживание
                    </h2>
                    <div class="methods-grid">
                        {% for method in methods_utilities %}
                        <div class="method-card">
                            <div class="method-header">
                                <div class="method-icon">
                                    <i class="{{ method.icon }}"></i>
                                </div>
                                <div class="method-name">{{ method.name }}</div>
                            </div>
                            <div class="method-endpoint">
                                <span class="method-method method-{{ method.method.lower() }}">{{ method.method }}</span>
                                {{ method.endpoint }}
                            </div>
                            <div class="method-description">{{ method.description }}</div>
                            {% if method.method == 'POST' %}
                                <button class="btn btn-post" onclick="callEndpoint('{{ method.endpoint }}', 'POST', '{{ method.name }}')">
                                    <i class="fas fa-play"></i>Выполнить
                                </button>
                            {% else %}
                                <a class="btn btn-get" href="{{ method.endpoint }}" target="_blank">
                                    <i class="fas fa-external-link-alt"></i>Выполнить
                                </a>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                </section>

                <!-- Status Section -->
                <section id="status">
                    <div class="status-section">
                        <div class="status-header">
                            <h2>
                                <i class="fas fa-heartbeat"></i>
                                Статус системы
                            </h2>
                            <button class="btn btn-refresh" onclick="checkStatus()">
                                <i class="fas fa-sync-alt"></i>Обновить
                            </button>
                        </div>
                        <div id="status-result">
                            <div class="no-processes">Нажмите "Обновить" для проверки статуса процессов</div>
                        </div>
                    </div>
                </section>

                <div class="footer">
                    &copy; 2024 Aerometr System | Версия 2.0 | Панель управления
                </div>
            </div>
        </div>
    </div>

    <script>
        async function callEndpoint(endpoint, method, methodName) {
            try {
                const btn = event.target;
                const originalText = btn.innerHTML;
                btn.innerHTML = '<div class="loading"></div> Выполняется...';
                btn.disabled = true;

                const response = await fetch(endpoint, { 
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    showNotification(`✅ ${methodName}: ${data.message || 'Операция выполнена успешно!'}`, 'success');
                } else {
                    showNotification(`❌ ${methodName}: ${data.error || 'Произошла ошибка'}`, 'error');
                }

            } catch (error) {
                showNotification(`❌ Ошибка соединения: ${error}`, 'error');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        function showNotification(message, type) {
            // Создаем уведомление
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                z-index: 10000;
                max-width: 400px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
                ${type === 'success' ? 'background: #4cc9f0;' : 'background: #e63946;'}
            `;
            notification.textContent = message;
            document.body.appendChild(notification);

            // Автоматическое удаление через 5 секунд
            setTimeout(() => {
                notification.remove();
            }, 5000);
        }

        async function checkStatus() {
            try {
                const statusDiv = document.getElementById('status-result');
                statusDiv.innerHTML = '<div class="no-processes"><div class="loading"></div> Загрузка...</div>';

                const response = await fetch('/background_status');
                const data = await response.json();

                if (data.background_processes && Object.keys(data.background_processes).length > 0) {
                    let html = '<div class="status-list">';
                    for (const [name, info] of Object.entries(data.background_processes)) {
                        const statusClass = info.is_alive ? '' : 'inactive';
                        const statusIcon = info.is_alive ? '🔵' : '⚪';
                        html += `
                            <div class="status-item ${statusClass}">
                                <div>
                                    <div class="status-name">${statusIcon} ${name}</div>
                                    <div class="status-details">
                                        Статус: ${info.status} | 
                                        Активен: ${info.is_alive ? 'Да' : 'Нет'} |
                                        Запущен: ${info.started_at}
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                    html += '</div>';
                    statusDiv.innerHTML = html;
                } else {
                    statusDiv.innerHTML = '<div class="no-processes">Нет активных фоновых процессов</div>';
                }
            } catch (error) {
                document.getElementById('status-result').innerHTML = 
                    '<div class="no-processes" style="color: #e63946;">Ошибка загрузки статуса</div>';
            }
        }

        // Плавная прокрутка для навигации
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Автоматическая проверка статуса при загрузке страницы
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(checkStatus, 1000);
        });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    """Главная страница со списком доступных методов в формате HTML"""

    methods_data_processing = [
        {
            'name': '🔄 Обновить статистику регионов',
            'endpoint': '/update_region_stats',
            'method': 'POST',
            'description': 'Запускает обновление статистики регионов (update_region_stats_main)',
            'icon': 'fas fa-chart-bar'
        },
        {
            'name': '📁 Обработать необработанные файлы',
            'endpoint': '/process_files',
            'method': 'POST',
            'description': 'Запускает обработку всех необработанных файлов (processor.process_all_files())',
            'icon': 'fas fa-file-process'
        },
        {
            'name': '✈️ Обновить данные aircraft',
            'endpoint': '/update_aircraft_data',
            'method': 'POST',
            'description': 'Запускает обновление данных о воздушных судах',
            'icon': 'fas fa-plane'
        },
        {
            'name': '🗺️ Запустить generate_grids',
            'endpoint': '/generate_grids',
            'method': 'POST',
            'description': 'Запускает генерацию сеток по настройкам',
            'icon': 'fas fa-th'
        },
        {
            'name': '🔄 Повторная обработка файла',
            'endpoint': '/reprocess',
            'method': 'GET',
            'description': 'Повторная обработка конкретного файла по имени (используйте /reprocess/имя_файла)',
            'icon': 'fas fa-redo'
        }
    ]

    methods_prediction = [
        {
            'name': '🔮 Генерация предсказаний',
            'endpoint': '/generate_predictions',
            'method': 'POST',
            'description': 'Генерирует предсказания полетов на указанный период (01.08.2025 - 31.12.2026)',
            'icon': 'fas fa-crystal-ball'
        },
        {
            'name': '📊 Статистика регионов',
            'endpoint': '/region_stats',
            'method': 'GET',
            'description': 'Получить статистику по регионам',
            'icon': 'fas fa-chart-pie'
        }
    ]

    methods_utilities = [
        {
            'name': '💾 Создать бэкап БД',
            'endpoint': '/create_backup',
            'method': 'POST',
            'description': 'Создает полную резервную копию базы данных',
            'icon': 'fas fa-database'
        },
        {
            'name': '🔑 Сгенерировать токен DataLens',
            'endpoint': '/generate_datalens_token',
            'method': 'GET',
            'description': 'Генерирует JWT токен для доступа к DataLens',
            'icon': 'fas fa-key'
        },
        {
            'name': '🔄 Обновить hexagon_id',
            'endpoint': '/update_hexagon_ids',
            'method': 'POST',
            'description': 'Обновляет hexagon_id в processed_flights',
            'icon': 'fas fa-sync'
        },
        {
            'name': '📐 Обработать полигоны',
            'endpoint': '/process_polygons',
            'method': 'POST',
            'description': 'Запускает обработку полигонов регионов',
            'icon': 'fas fa-draw-polygon'
        },
        {
            'name': '📋 Список методов (JSON)',
            'endpoint': '/api',
            'method': 'GET',
            'description': 'Возвращает список всех методов в формате JSON',
            'icon': 'fas fa-code'
        },
        {
            'name': '📊 Статус фоновых процессов',
            'endpoint': '/background_status',
            'method': 'GET',
            'description': 'Показывает статус запущенных фоновых процессов',
            'icon': 'fas fa-heartbeat'
        }
    ]

    return render_template_string(HTML_TEMPLATE,
                                  methods_data_processing=methods_data_processing,
                                  methods_prediction=methods_prediction,
                                  methods_utilities=methods_utilities)


@app.route('/api')
def api_index():
    """API страница со списком методов в формате JSON"""
    methods = [
        {
            'name': 'Обновить статистику регионов',
            'endpoint': '/update_region_stats',
            'method': 'POST',
            'description': 'Запускает обновление статистики регионов'
        },
        {
            'name': 'Обработать необработанные файлы',
            'endpoint': '/process_files',
            'method': 'POST',
            'description': 'Запускает обработку всех необработанных файлов'
        },
        {
            'name': 'Обновить данные aircraft',
            'endpoint': '/update_aircraft_data',
            'method': 'POST',
            'description': 'Запускает обновление данных о воздушных судах'
        },
        {
            'name': 'Запустить generate_grids',
            'endpoint': '/generate_grids',
            'method': 'POST',
            'description': 'Запускает генерацию сеток по настройкам'
        },
        {
            'name': 'Повторная обработка файла',
            'endpoint': '/reprocess/<filename>',
            'method': 'GET',
            'description': 'Повторная обработка конкретного файла по имени'
        },
        {
            'name': 'Генерация предсказаний',
            'endpoint': '/generate_predictions',
            'method': 'POST',
            'description': 'Генерирует предсказания полетов'
        },
        {
            'name': 'Создать бэкап БД',
            'endpoint': '/create_backup',
            'method': 'POST',
            'description': 'Создает полную резервную копию базы данных'
        },
        {
            'name': 'Статус фоновых процессов',
            'endpoint': '/background_status',
            'method': 'GET',
            'description': 'Показывает статус запущенных фоновых процессов'
        }
    ]

    return jsonify({
        "message": "Добро пожаловать в API системы Aerometr",
        "available_methods": methods,
        "version": "2.0"
    })


# Существующие методы (сохранены из оригинального app.py)
@app.route('/update_region_stats', methods=['POST'])
def update_region_stats():
    """Запуск обновления статистики регионов"""
    try:
        def run_update():
            update_region_stats_main()

        thread = threading.Thread(target=run_update, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['update_region_stats'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Обновление статистики регионов запущено",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/process_files', methods=['POST'])
def process_files():
    """Запуск обработки необработанных файлов"""
    try:
        processor = FlightDataProcessor()
        if not processor.connect_to_db():
            return jsonify({"error": "Не удалось подключиться к базе данных"}), 500

        def run_processing():
            processor.process_all_files()

        thread = threading.Thread(target=run_processing, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['process_files'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Обработка файлов запущена",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_aircraft_data', methods=['POST'])
def update_aircraft_data():
    """Запуск обновления данных о воздушных судах"""
    try:
        db_manager = DatabaseManager(DB_CONFIG)
        if not db_manager.connection_pool:
            return jsonify({"error": "Не удалось инициализировать пул соединений для aircraft"}), 500

        opensky_client = OpenSkyClient()
        aircraft_processor = AircraftDataProcessor(db_manager)
        scheduler = Scheduler(db_manager, opensky_client, aircraft_processor)

        def run_aircraft_update():
            scheduler.fetch_and_save_aircraft_data()

        thread = threading.Thread(target=run_aircraft_update, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['update_aircraft_data'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Обновление данных aircraft запущено",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate_grids', methods=['POST'])
def generate_grids():
    """Запуск генерации сеток"""
    try:
        generator = GridGenerator(DB_CONFIG)

        def run_grid_generation():
            russia_bbox = (41.0, 19.0, 82.0, 180.0)
            generator.generate_grids(russia_bbox)

        thread = threading.Thread(target=run_grid_generation, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['generate_grids'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Генерация сеток запущена",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reprocess/<path:filename>')
def reprocess_file(filename):
    """Повторная обработка файла по имени"""
    try:
        processor = FlightDataProcessor()
        if not processor.connect_to_db():
            return jsonify({"error": "Не удалось подключиться к базе данных"}), 500

        cursor = processor.connection.cursor()
        cursor.execute("""
            UPDATE processed_files 
            SET status = 'pending', error_message = NULL, procent = 0.00 
            WHERE filename = %s
        """, (filename,))
        processor.connection.commit()
        cursor.close()

        def run_reprocessing():
            processor.process_unprocessed_files()

        thread = threading.Thread(target=run_reprocessing, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads[f'reprocess_{filename}'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": f"Файл '{filename}' отправлен на повторную обработку",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reprocess')
def reprocess_info():
    """Информация о повторной обработке файлов"""
    return jsonify({
        "message": "Для повторной обработки файла используйте /reprocess/имя_файла",
        "example": "/reprocess/report_2024.xlsx"
    })


# Новые методы
@app.route('/generate_predictions', methods=['POST'])
def generate_predictions():
    """Запуск генерации предсказаний"""
    try:
        predictor = FlightPredictorNew(DB_CONFIG)

        def run_prediction():
            success = predictor.generate_predictions(
                prediction_start='2025-08-01',
                prediction_end='2025-12-31'
            )
            return success

        thread = threading.Thread(target=run_prediction, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['generate_predictions'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Генерация предсказаний запущена (период: 2025-08-01 - 2025-12-31)",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/create_backup', methods=['POST'])
def create_backup():
    """Создание бэкапа базы данных"""
    try:
        def run_backup():
            creator = BackupCreator(DB_CONFIG)
            backup_name = creator.create_backup()
            return backup_name

        thread = threading.Thread(target=run_backup, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['create_backup'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Создание бэкапа базы данных запущено",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate_datalens_token', methods=['GET'])
def generate_datalens_token():
    """Генерация JWT токена для DataLens"""
    try:
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
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_hexagon_ids', methods=['POST'])
def update_hexagon_ids():
    """Обновление hexagon_id в processed_flights"""
    try:
        generator = GridGenerator(DB_CONFIG)

        def run_update():
            updated_count = generator.update_processed_flights_hexagon_id_simple()
            return updated_count

        thread = threading.Thread(target=run_update, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['update_hexagon_ids'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Обновление hexagon_id запущено",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/process_polygons', methods=['POST'])
def process_polygons():
    """Обработка полигонов регионов"""
    try:
        db_manager = DatabaseManager(DB_CONFIG)
        if not db_manager.connection_pool:
            return jsonify({"error": "Не удалось инициализировать пул соединений"}), 500

        def run_polygon_processing():
            polygon_processor = PolygonProcessor(db_manager)
            polygon_processor.set_points_polygon()
            polygon_processor.calculate_intersections()

        thread = threading.Thread(target=run_polygon_processing, daemon=True)
        thread.start()

        with background_threads_lock:
            background_threads['process_polygons'] = {
                'thread': thread,
                'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'running'
            }

        return jsonify({
            "message": "Обработка полигонов запущена",
            "status": "started"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/region_stats', methods=['GET'])
def get_region_stats():
    """Получение статистики по регионам"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT region, date, total_flights, flight_density, peak_load
            FROM region_stats 
            ORDER BY date DESC, total_flights DESC 
            LIMIT 100
        """)

        stats = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "stats": stats,
            "total_records": len(stats)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/background_status')
def background_status():
    """Показывает статус фоновых процессов"""
    with background_threads_lock:
        status_info = {}
        for name, info in background_threads.items():
            status_info[name] = {
                'status': info['status'],
                'is_alive': info['thread'].is_alive() if 'thread' in info else False,
                'started_at': info.get('started_at', 'unknown')
            }

    return jsonify({
        "background_processes": status_info,
        "total_processes": len(status_info),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)