# main.py
"""
Главный модуль программы. Запускает обработку файлов с FTP и обновление статистики.
Создает отдельный поток для выполнения операций.
"""
import threading
import logging
from parser.parser_file import FlightDataProcessor
from parser.region_stats_updater import update_region_stats_main

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parser/log.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def process_files():
    """Запуск обработки файлов и обновления статистики"""
    processor = FlightDataProcessor()
    processor.process_all_files()
    update_region_stats_main()

def main():
    """Основная функция запуска в отдельном потоке"""
    thread = threading.Thread(target=process_files)
    thread.daemon = True
    thread.start()
    thread.join()

if __name__ == "__main__":
    main()