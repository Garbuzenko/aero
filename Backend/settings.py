# settings.py
"""
Настройки приложения.
Содержит конфигурацию базы данных и FTP.
"""

# Конфигурация базы данных
DB_CONFIG = {
    'user': 'u3253297_hack',
    'password': 'ПАРОЛЬ У АВТОРА',
    'host': '31.31.197.64',
    'port': '3306',
    'database': 'u3253297_hack',
    'raise_on_warnings': True,
    'connect_timeout': 30000,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

FUSION_BRAIN = {
    'api_key':"1CFBC09CEC6BA676965AA5BA35BD901C",
    'secret_key':"ПАРОЛЬ У АВТОРА"
}


GIGACHAT_CREDENTIALS = {
    'client_id':"913e9ea0-04e6-4b2a-b468-0e62f9356064",
    'client_secret':"ПАРОЛЬ У АВТОРА"
}

# Данные для FTP
FTP_CONFIG = {
    'host': '31.31.197.64',
    'username': 'u3253297',
    'password': 'ПАРОЛЬ У АВТОРА',
    'remote_dir': '/www/aerometr.ru/files/',
}

private_key = b"""ПАРОЛЬ У АВТОРА"""