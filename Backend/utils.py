import os
import re
import mysql.connector
from mysql.connector import Error
from settings import DB_CONFIG

# УКАЖИТЕ КОРЕНЬ ВАШЕГО ПРОЕКТА ЗДЕСЬ
# Например, если utils.py лежит в папке aerometr, то:
root_path = os.path.dirname(os.path.abspath(__file__))  # <-- корень проекта

output_file = "combined_code.txt"
gitignore_path = os.path.join(root_path, '.gitignore')

# Расширения текстовых файлов для включения
TEXT_EXTENSIONS = {
    '.py'
}

# Системные и служебные директории, которые нужно игнорировать всегда
SYSTEM_DIRS_TO_IGNORE = {
    '.git', '.svn', '.hg', '__pycache__', '.mypy_cache', '.pytest_cache',
    '.venv', 'venv', 'env', 'node_modules', '.idea', '.vscode',
    '.DS_Store', 'Thumbs.db', 'build', 'dist', 'logs',
    # Служебные папки Windows (на случай, если root_path — не корень диска)
    '$RECYCLE.BIN', 'System Volume Information', 'Recovery', 'PerfLogs'
}


def parse_gitignore(gitignore_path):
    """Парсит .gitignore файл и возвращает список шаблонов для исключения"""
    ignore_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Убираем начальный слэш (если есть) — gitignore работает относительно корня
                if line.startswith('/'):
                    line = line[1:]
                # Убираем экранирование обратного слэша в начале
                if line.startswith('\\'):
                    line = line[1:]
                ignore_patterns.append(line)
    return ignore_patterns


def should_ignore(path, ignore_patterns, is_dir=False):
    """Проверяет, должен ли файл/папка быть проигнорирован по правилам .gitignore"""
    try:
        rel_path = os.path.relpath(path, root_path).replace('\\', '/')  # унифицируем слэши
    except ValueError:
        # На Windows: если path и root_path на разных дисках — relpath не работает
        return True

    for pattern in ignore_patterns:
        # Пропускаем пустые шаблоны
        if not pattern:
            continue

        # Обработка шаблонов, заканчивающихся на /
        if pattern.endswith('/'):
            if not is_dir:
                continue
            regex_pattern = pattern[:-1]
        else:
            regex_pattern = pattern

        # Преобразуем gitignore-шаблон в regex
        # Экранируем спецсимволы, кроме * и ?
        regex_pattern = re.escape(regex_pattern)
        regex_pattern = regex_pattern.replace(r'\*', '.*').replace(r'\?', '.')
        # Поддержка ** (рекурсивное совпадение)
        regex_pattern = regex_pattern.replace(r'\.\*', '.*')
        regex_pattern = regex_pattern.replace(r'.*', '.*')  # убедимся, что * → .*

        # Шаблоны без / в начале применяются рекурсивно ко всем подпапкам
        if not pattern.startswith('/'):
            full_regex = r'.*/' + regex_pattern + r'$'
        else:
            full_regex = '^' + regex_pattern + r'$'

        try:
            if re.fullmatch(full_regex, rel_path, re.IGNORECASE):
                return True
        except re.error:
            # Некорректный regex — пропускаем шаблон
            continue

    return False


def is_text_file(file_path):
    """Проверяет, является ли файл текстовым (по расширению и содержимому)"""
    if not os.path.isfile(file_path):
        return False

    ext = os.path.splitext(file_path)[1].lower()
    if ext in TEXT_EXTENSIONS:
        return True


def get_database_schema():
    """Подключается к БД и получает схему всех таблиц"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()

            # Получаем имя текущей базы данных
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]

            # Получаем список таблиц в текущей БД (исключая служебные)
            cursor.execute("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = %s
                  AND TABLE_TYPE = 'BASE TABLE'
                  AND TABLE_NAME NOT LIKE '\\_%%'
            """, (db_name,))
            tables = [row[0] for row in cursor.fetchall()]

            schema = "# ===== СХЕМА БАЗЫ ДАННЫХ =====\n\n"

            if not tables:
                schema += "# Нет таблиц в базе данных.\n"
            else:
                for table_name in tables:
                    # Валидация имени таблицы (только буквы, цифры, подчёркивание)
                    if not re.match(r'^[a-zA-Z0-9_]+$', table_name):
                        schema += f"# Пропущена таблица с недопустимым именем: {table_name}\n"
                        continue
                    # Безопасное выполнение SHOW CREATE TABLE
                    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                    result = cursor.fetchone()
                    if result:
                        create_stmt = result[1]
                        schema += f"# Таблица: {table_name}\n"
                        schema += f"{create_stmt};\n\n"

            cursor.close()
            connection.close()
            return schema

    except Error as e:
        return f"# Ошибка при подключении к БД: {e}\n"
    except Exception as e:
        return f"# Неизвестная ошибка при получении схемы БД: {e}\n"


# === ОСНОВНОЙ КОД ===

ignore_patterns = parse_gitignore(gitignore_path)

# Убедимся, что выходной файл пуст
with open(output_file, "w", encoding="utf-8") as outfile:
    pass

with open(output_file, "a", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk(root_path):
        # Удаляем из обхода системные и игнорируемые директории
        dirs[:] = [
            d for d in dirs
            if d not in SYSTEM_DIRS_TO_IGNORE
            and not should_ignore(os.path.join(root, d), ignore_patterns, is_dir=True)
        ]

        for file in files:
            file_path = os.path.join(root, file)

            # Пропускаем сам utils.py
            if os.path.abspath(file_path) == os.path.abspath(__file__):
                continue

            rel_path = os.path.relpath(file_path, root_path).replace('\\', '/')

            # Проверка на игнорирование
            if (should_ignore(file_path, ignore_patterns) or
                not is_text_file(file_path)):
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors='ignore') as infile:
                    content = infile.read()
                outfile.write(f"\n\n{'=' * 50}\n# Файл: {rel_path}\n{'=' * 50}\n\n")
                outfile.write(content)
            except Exception as e:
                print(f"Ошибка при обработке файла {rel_path}: {e}")

    # Добавляем схему базы данных в конец
    db_schema = get_database_schema()
    outfile.write("\n\n")
    outfile.write(db_schema)

print(f"Текстовые файлы проекта из '{root_path}' объединены в '{output_file}'")