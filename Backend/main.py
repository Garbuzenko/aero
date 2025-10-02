# main.py
"""
Главный модуль программы.
Запускает:
- фоновую обработку файлов (каждые 5 сек проверка processed_files)
- фоновое обновление данных о воздушных судах (каждые 600 сек)
"""
import threading
import time
import logging

from aircraft.aircraft import Scheduler
from parser.parser_file import FlightDataProcessor
from parser.region_stats_updater import update_region_stats_main
# from aircraft import Scheduler
from settings import DB_CONFIG

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def check_and_process_files():
    """Проверяет таблицу processed_files каждые 5 сек и запускает обработку при наличии необработанных файлов."""

    processor = FlightDataProcessor()
    if not processor.connect_to_db():
        logging.error("Не удалось подключиться к БД для проверки файлов")
        return

    while True:
        try:
            cursor = processor.connection.cursor()
            cursor.execute("""
                SELECT filename FROM processed_files 
                WHERE status != 'processed'
            """)
            unprocessed = cursor.fetchall()
            cursor.close()
            print('check_and_process_files')
            if unprocessed:
                logging.info(f"Обнаружено {len(unprocessed)} необработанных файлов. Запуск обработки...")
                processor.process_all_files()
                # После обработки обновляем статистику регионов
                update_region_stats_main()
            else:
                logging.debug("Нет необработанных файлов.")

        except Exception as e:
            logging.error(f"Ошибка при проверке необработанных файлов: {e}")

        time.sleep(2)  # Пауза 5 секунд


def start_aircraft_scheduler():
    """Запускает фоновый сбор данных о воздушных судах."""
    from aircraft.opensky_client import OpenSkyClient
    from aircraft.aircraft import DatabaseManager, AircraftDataProcessor

    db_manager = DatabaseManager(DB_CONFIG)
    if not db_manager.connection_pool:
        logging.error("Не удалось инициализировать пул соединений для aircraft")
        return

    opensky_client = OpenSkyClient()
    aircraft_processor = AircraftDataProcessor(db_manager)
    scheduler = Scheduler(db_manager, opensky_client, aircraft_processor)
    aircraft_thread = scheduler.start_aircraft_data_thread(interval=600)
    logging.info("Поток сбора данных aircraft запущен (интервал: 600 сек)")

    # Ждём завершения (в реальном приложении можно использовать более гибкую логику)
    aircraft_thread.join()


def main():
    """Запускает два фоновых потока."""
    # Поток обработки файлов
    file_thread = threading.Thread(target=check_and_process_files, daemon=True)
    file_thread.start()

    # Поток обновления данных aircraft
    aircraft_thread = threading.Thread(target=start_aircraft_scheduler, daemon=True)
    aircraft_thread.start()

    # Основной цикл — чтобы программа не завершалась
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Получен сигнал завершения. Завершение работы...")


if __name__ == "__main__":
    main()