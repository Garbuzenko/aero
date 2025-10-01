# fusionbrain_generator.py
import mysql.connector
import base64
import time
import requests
import json

from utils import settings
from utils.settings import DB_CONFIG


class FusionBrainRegionGenerator:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = "https://api-key.fusionbrain.ai/"
        self.auth_headers = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_db_connection(self):
        """Установка соединения с базой данных"""
        return mysql.connector.connect(**DB_CONFIG)

    def get_regions(self, limit=1):
        """Получение списка регионов из БД с ограничением количества"""
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, name, federal_district FROM regions LIMIT %s"
        cursor.execute(query, (limit,))
        regions = cursor.fetchall()

        cursor.close()
        conn.close()
        return regions

    def get_model_id(self):
        """Получение ID доступного пайплайна для генерации"""
        response = requests.get(
            self.url + 'key/api/v1/pipelines',
            headers=self.auth_headers
        )
        response.raise_for_status()
        pipelines = response.json()

        # Ищем пайплайн для генерации изображений
        for pipeline in pipelines:
            if pipeline['type'] == 'TEXT2IMAGE':
                return pipeline['id']

        raise Exception("No TEXT2IMAGE pipeline found")

    def generate_image(self, prompt, pipeline_id):
        """Запрос на генерацию изображения через API"""
        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": 1024,
            "height": 1024,
            "generateParams": {
                "query": prompt
            }
        }

        data = {
            'pipeline_id': (None, pipeline_id),
            'params': (None, json.dumps(params), 'application/json')
        }

        response = requests.post(
            self.url + 'key/api/v1/pipeline/run',
            headers=self.auth_headers,
            files=data
        )
        response.raise_for_status()
        return response.json()['uuid']

    def wait_for_generation(self, task_id, max_attempts=30, delay=10):
        """Ожидание завершения генерации изображения"""
        for attempt in range(max_attempts):
            response = requests.get(
                self.url + 'key/api/v1/pipeline/status/' + task_id,
                headers=self.auth_headers
            )
            response.raise_for_status()
            status_data = response.json()

            if status_data['status'] == 'DONE':
                return status_data['result']['files'][0]
            elif status_data['status'] == 'FAIL':
                raise Exception(f"Generation failed: {status_data.get('errorDescription', 'Unknown error')}")

            time.sleep(delay)

        raise Exception("Generation timeout exceeded")

    def save_image(self, image_data, filename):
        """Сохранение изображения из base64 в файл"""
        image_bytes = base64.b64decode(image_data)
        with open(filename, 'wb') as file:
            file.write(image_bytes)

    def process_regions(self, limit=1):
        """Основной метод обработки регионов"""
        try:
            # Получаем регионы из БД
            regions = self.get_regions(limit)
            print(f"Found {len(regions)} regions to process")

            # Получаем ID модели
            model_id = self.get_model_id()
            print(f"Using model ID: {model_id}")

            # Обрабатываем каждый регион
            for region in regions:
                region_id = region['id']
                region_name = region['name']
                district = region['federal_district']

                print(f"Processing region: {region_name} (ID: {region_id})")

                # Создаем промпт для генерации
                prompt = (f"Фото достопримечательность {region_name} красивый стиль аниме")
                print(prompt)

                # Генерируем изображение
                task_id = self.generate_image(prompt, model_id)
                print(f"Generation started for {region_name}, task ID: {task_id}")

                # Ждем завершения
                image_data = self.wait_for_generation(task_id)

                # Сохраняем изображение
                filename = f"{region_id}.jpg"
                self.save_image(image_data, filename)
                print(f"Image saved as {filename}")

        except Exception as e:
            print(f"Error processing regions: {str(e)}")
            raise


# Пример использования
if __name__ == "__main__":
    # Инициализация генератора (ключи нужно заменить на реальные)
    generator = FusionBrainRegionGenerator(
        api_key=settings.FUSION_BRAIN['api_key'],
        secret_key=settings.FUSION_BRAIN['secret_key']
    )

    # Обработка одного региона
    generator.process_regions(limit=85)