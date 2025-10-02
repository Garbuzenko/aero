# settings.py
"""
Настройки приложения.
Содержит конфигурацию базы данных и FTP.
"""

# Конфигурация базы данных
DB_CONFIG = {
    'user': 'u3253297_hack',
    'password': 'ПАРОЛЬ',
    'host': '31.31.197.64',
    'port': '3306',
    'database': 'u3253297_hack',
    'raise_on_warnings': True,
    'connect_timeout': 30000,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

FUSION_BRAIN = {
    'api_key':"ПАРОЛЬ",
    'secret_key':"ПАРОЛЬ"
}


GIGACHAT_CREDENTIALS = {
    'client_id':"ПАРОЛЬ",
    'client_secret':"ПАРОЛЬ"
}

# Данные для FTP
FTP_CONFIG = {
    'host': '31.31.197.64',
    'username': 'u3253297',
    'password': 'ПАРОЛЬ',
    'remote_dir': '/www/aerometr.ru/files/',
}

private_key = b"""-----BEGIN RSA PRIVATE KEY-----
ПАРОЛЬ
-----END RSA PRIVATE KEY-----"""