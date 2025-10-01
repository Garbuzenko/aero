# backup.py
import mysql.connector
from mysql.connector import Error
import datetime
from settings import DB_CONFIG


class BackupCreator:
    def __init__(self, db_config):
        self.original_db = db_config['database']
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def create_backup_db_name(self):
        """Генерирует имя для базы данных бэкапа"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.original_db}_backup"

    def connect(self):
        """Устанавливает соединение с базой данных"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("Успешное подключение к базе данных")
        except Error as e:
            print(f"Ошибка подключения: {e}")
            raise

    def disconnect(self):
        """Закрывает соединение с базой данных"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("Соединение с базой данных закрыто")

    def backup_database_exists(self, backup_db_name):
        """Проверяет, существует ли база данных бэкапа"""
        try:
            self.cursor.execute("SHOW DATABASES LIKE %s", (backup_db_name,))
            return self.cursor.fetchone() is not None
        except Error as e:
            print(f"Ошибка при проверке существования базы данных: {e}")
            return False

    def create_backup_database(self, backup_db_name):
        """Создает новую базу данных для бэкапа"""
        try:
            # Если база данных уже существует, удаляем ее
            if self.backup_database_exists(backup_db_name):
                self.cursor.execute(f"DROP DATABASE {backup_db_name}")
                print(f"Удалена существующая база данных бэкапа: {backup_db_name}")

            self.cursor.execute(f"CREATE DATABASE {backup_db_name}")
            print(f"Создана база данных для бэкапа: {backup_db_name}")
        except Error as e:
            print(f"Ошибка при создании базы данных: {e}")
            raise

    def get_tables_list(self):
        """Получает список таблиц в исходной базе данных"""
        self.cursor.execute("SHOW TABLES")
        return [table[0] for table in self.cursor.fetchall()]

    def table_exists_in_backup(self, backup_db_name, table_name):
        """Проверяет, существует ли таблица в базе данных бэкапа"""
        try:
            self.cursor.execute(f"""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = %s
            """, (backup_db_name, table_name))
            return self.cursor.fetchone()[0] > 0
        except Error as e:
            print(f"Ошибка при проверке существования таблицы: {e}")
            return False

    def copy_tables(self, backup_db_name):
        """Копирует все таблицы и данные в новую базу данных"""
        tables = self.get_tables_list()

        # Отключаем проверку внешних ключей для ускорения копирования
        self.cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        for table in tables:
            try:
                # Проверяем, существует ли таблица в бэкапе, и удаляем если существует
                if self.table_exists_in_backup(backup_db_name, table):
                    self.cursor.execute(f"DROP TABLE {backup_db_name}.{table}")
                    print(f"Удалена существующая таблица в бэкапе: {table}")

                # Создаем структуру таблицы
                self.cursor.execute(f"CREATE TABLE {backup_db_name}.{table} LIKE {self.original_db}.{table}")

                # Копируем данные
                self.cursor.execute(f"INSERT INTO {backup_db_name}.{table} SELECT * FROM {self.original_db}.{table}")

                print(f"Скопирована таблица: {table}")
            except Error as e:
                print(f"Ошибка при копировании таблицы {table}: {e}")
                # Можно выбрать: продолжить с другими таблицами или прервать процесс
                # raise  # Раскомментируйте, чтобы прервать при ошибке

        # Включаем проверку внешних ключей обратно
        self.cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        self.connection.commit()

    def create_backup(self):
        """Основной метод для создания бэкапа"""
        try:
            self.connect()
            backup_db_name = self.create_backup_db_name()
            self.create_backup_database(backup_db_name)
            self.copy_tables(backup_db_name)
            print(f"Бэкап успешно создан в базе: {backup_db_name}")
            return backup_db_name
        except Exception as e:
            print(f"Ошибка при создании бэкапа: {e}")
            return None
        finally:
            self.disconnect()


# Пример использования
if __name__ == "__main__":
    creator = BackupCreator(DB_CONFIG)
    creator.create_backup()