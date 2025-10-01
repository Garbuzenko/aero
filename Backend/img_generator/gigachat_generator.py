import mysql.connector
import time
import requests
import json
import uuid
import base64
import os
import re
from bs4 import BeautifulSoup

from utils import settings
from utils.settings import DB_CONFIG


class GigaChatRegionGenerator:
    def __init__(self):
        # Получаем учетные данные из настроек
        self.client_id = settings.GIGACHAT_CREDENTIALS['client_id']
        self.client_secret = settings.GIGACHAT_CREDENTIALS['client_secret']

        # Указываем путь к российским сертификатам
        self.cert_path = r"D:\hack\python\hack2025\python\windows_russian_trusted_root_ca\russian_trusted_root_ca_pem.crt"

        # Устанавливаем переменные окружения для использования российских сертификатов
        os.environ['SSL_CERT_FILE'] = self.cert_path
        os.environ['REQUESTS_CA_BUNDLE'] = self.cert_path

        # Базовые URL для API
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self.token_expires = 0

    def get_db_connection(self):
        """Установка соединения с базой данных"""
        return mysql.connector.connect(**DB_CONFIG)

    def get_regions(self, limit=1):
        """Получение списка регионов из БД с ограничением количества"""
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, name, federal_district FROM regions WHERE id>92 LIMIT %s"
        cursor.execute(query, (limit,))
        regions = cursor.fetchall()

        cursor.close()
        conn.close()
        return regions

    def get_access_token(self):
        """Получение access token с использованием российских сертификатов"""
        if self.access_token and time.time() < self.token_expires:
            return self.access_token

        # Создаем Basic Auth заголовок
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f'Basic {auth_base64}'
        }

        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }

        try:
            # Используем российские сертификаты для аутентификации
            response = requests.post(
                self.auth_url,
                headers=headers,
                data=payload,
                verify=self.cert_path,
                timeout=30
            )
        except requests.exceptions.SSLError:
            # Резервный вариант без проверки SSL
            response = requests.post(
                self.auth_url,
                headers=headers,
                data=payload,
                verify=False,
                timeout=30
            )

        if response.status_code != 200:
            error_msg = f"Ошибка аутентификации: {response.status_code}"
            if response.text:
                error_msg += f" - {response.text}"
            raise Exception(error_msg)

        try:
            token_data = response.json()
            self.access_token = token_data.get('access_token')

            if not self.access_token:
                raise Exception("Access token не получен в ответе")

            # Устанавливаем время истечения токена
            self.token_expires = time.time() + 1800 - 60  # 30 минут - 60 секунд запаса

            return self.access_token
        except json.JSONDecodeError:
            raise Exception(f"Неверный формат ответа от сервера: {response.text}")

    def generate_image(self, prompt: str):
        """Генерация изображения через прямой запрос к GigaChat API"""
        try:
            # Получаем access token
            access_token = self.get_access_token()

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            # Создаем промпт с явным указанием на генерацию изображения
            image_prompt = f"Нарисуй: {prompt}"

            payload = {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "user",
                        "content": image_prompt
                    }
                ],
                "function_call": "auto"  # Важный параметр для активации генерации изображений:cite[2]
            }

            # Отправляем запрос к API генерации изображений
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                verify=self.cert_path,
                timeout=60
            )

            if response.status_code != 200:
                error_msg = f"Ошибка генерации изображения: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)

            response_data = response.json()

            # Извлекаем контент из ответа
            content = response_data['choices'][0]['message']['content']
            print(f"Ответ API: {content}")

            # Пытаемся найти идентификатор изображения в ответе:cite[2]
            if '<img' in content:
                soup = BeautifulSoup(content, "html.parser")
                img_tag = soup.find('img')

                if img_tag and img_tag.get('src'):
                    file_id = img_tag.get('src')
                    print(f"Найден идентификатор изображения: {file_id}")
                    return file_id
                else:
                    raise Exception("В ответе найден тег img, но отсутствует идентификатор изображения")
            else:
                # Если в ответе нет тега img, возможно, API вернуло другой формат
                # Попробуем извлечь идентификатор другим способом
                if 'img' in content.lower() or 'src=' in content.lower():
                    # Пытаемся найти UUID в тексте ответа
                    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
                    uuids = re.findall(uuid_pattern, content)
                    if uuids:
                        print(f"Найден UUID в ответе: {uuids[0]}")
                        return uuids[0]

                raise Exception(f"Ответ не содержит идентификатор изображения. Полный ответ: {content}")

        except Exception as e:
            print(f"Ошибка при генерации изображения: {str(e)}")
            raise

    def download_image(self, file_id: str, filename: str):
        """Скачивание изображения по идентификатору файла с использованием GET запроса:cite[2]"""
        try:
            # Получаем access token
            access_token = self.get_access_token()

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }

            # Формируем URL для скачивания изображения
            download_url = f"{self.api_url}/files/{file_id}/content"

            # Отправляем GET запрос на скачивание (как указано в документации):cite[2]
            response = requests.get(
                download_url,
                headers=headers,
                verify=self.cert_path,
                timeout=30
            )

            if response.status_code != 200:
                error_msg = f"Ошибка загрузки изображения: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)

            # Сохраняем изображение
            with open(filename, 'wb') as file:
                file.write(response.content)

            return True

        except Exception as e:
            print(f"Ошибка при скачивании изображения: {str(e)}")
            return False

    def process_regions(self, limit=1):
        """Основной метод обработки регионов"""
        try:
            # Создаем папку для изображений, если её нет
            os.makedirs("img_gigachat", exist_ok=True)

            # Получаем регионы из БД
            regions = self.get_regions(limit)
            print(f"Найдено регионов для обработки: {len(regions)}")

            # Обрабатываем каждый регион
            for region in regions:
                region_id = region['id']
                region_name = region['name']
                district = region['federal_district']

                print(f"\nОбрабатывается регион: {region_name} (ID: {region_id})")

                # Создаем промпт для генерации
                prompt = f"Природа летом {region_name}"
                print(f"Промпт: {prompt}")

                try:
                    # Генерируем изображение и получаем идентификатор файла
                    file_id = self.generate_image(prompt)
                    print(f"Получен идентификатор файла: {file_id}")

                    # Формируем путь для сохранения
                    filename = f"img_gigachat/{region_id}.jpg"

                    # Скачиваем и сохраняем изображение
                    if self.download_image(file_id, filename):
                        print(f"Изображение успешно сохранено как {filename}")
                    else:
                        print(f"Не удалось скачать изображение для {region_name}")

                except Exception as e:
                    print(f"Ошибка при обработке региона {region_name}: {str(e)}")
                    continue

                # Добавляем задержку между запросами
                time.sleep(2)

        except Exception as e:
            print(f"Ошибка обработки регионов: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        # Инициализация генератора
        generator = GigaChatRegionGenerator()

        # Проверяем соединение с GigaChat
        print("Проверка соединения с GigaChat API...")

        # Обработка регионов
        generator.process_regions(limit=4)

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        print("\nВозможные решения:")
        print("1. Проверьте правильность client_id и client_secret в settings.py")
        print("2. Убедитесь, что сертификаты находятся по указанному пути")
        print("3. Проверьте подключение к интернету")
        print("4. Убедитесь, что ваш аккаунт GigaChat имеет доступ к API генерации изображений")
        print("5. Проверьте, что в вашем тарифном плане включена функция генерации изображений")