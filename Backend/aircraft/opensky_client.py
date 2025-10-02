# opensky_client.py
import requests
import time
from datetime import datetime


class OpenSkyClient:
    def __init__(self, username=None, password=None):
        self.base_url = "https://opensky-network.org/api"
        self.auth = (username, password) if username and password else None
        self.session = requests.Session()
        self.session.timeout = 30

    def get_all_aircrafts(self, bbox=None):
        """Получить все самолеты в реальном времени"""
        url = f"{self.base_url}/states/all"
        params = {}

        if bbox:
            params['lamin'] = bbox[1]
            params['lamax'] = bbox[3]
            params['lomin'] = bbox[0]
            params['lomax'] = bbox[2]

        try:
            response = self.session.get(url, params=params, timeout=30)
            print(url)

            if response.status_code == 401:
                print("Ошибка 401: Попробуем без аутентификации...")
                response = requests.get(url, params=params, timeout=30)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            if 'response' in locals():
                print(f"Status Code: {response.status_code}")
                print(f"Response Text: {response.text[:200]}")
            return None

    def test_connection(self):
        """Тестирование подключения к OpenSky API"""
        print("Тестирование подключения к OpenSky API...")
        try:
            response = requests.get("https://opensky-network.org/api/states/all", timeout=30)
            print(f"Без аутентификации: Status {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                count = len(data['states']) if data and 'states' in data else 0
                print(f"Успешно! Найдено самолетов: {count}")
                return True
            return False
        except Exception as e:
            print(f"Ошибка тестирования: {e}")
            return False