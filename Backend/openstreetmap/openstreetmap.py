#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from settings import DB_CONFIG
import sys
import json
import time
import logging
from pprint import pprint
from typing import Dict, Any, Optional
import requests
import mysql.connector
from mysql.connector import Error
from shapely.geometry import shape
import osm2geojson

# === ЛОГИРОВАНИЕ ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('../log/russia_boundaries_loader.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# # === НАСТРОЙКИ ===
# try:
#     from utils.settings import DB_CONFIG
# except ImportError:
#     logger.error("❌ Не найден файл settings.py или отсутствует DB_CONFIG")
#     sys.exit(1)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

ADMIN_LEVELS = {
    "federal_districts": "4",
    "regions": "6",
    "municipalities": "8"
}

def get_admin_type(admin_level: str) -> str:
    mapping = {
        '2': 'Страна',
        '3': 'Международный союз',
        '4': 'Федеральный округ',
        '5': 'Регион (группа субъектов)',
        '6': 'Субъект Федерации',
        '7': 'Городской округ',
        '8': 'Муниципальный район',
        '9': 'Городское поселение',
        '10': 'Сельское поселение'
    }
    return mapping.get(admin_level, 'Неизвестно')


def extract_geopolygon_coords(geom: dict) -> Optional[list]:
    """
    Преобразует GeoJSON-геометрию (Polygon или MultiPolygon)
    в список колец в формате [[lat, lon], ...], готовый для GEOPOLYGON в DataLens.
    Возвращает None при ошибке.
    """
    try:
        if geom['type'] == 'Polygon':
            # Один полигон: массив колец (внешнее + дырки)
            return [
                [[round(coord[1], 6), round(coord[0], 6)] for coord in ring]
                for ring in geom['coordinates']
            ]
        elif geom['type'] == 'MultiPolygon':
            # Несколько полигонов: каждый — массив колец
            result = []
            for polygon in geom['coordinates']:
                rings = [
                    [[round(coord[1], 6), round(coord[0], 6)] for coord in ring]
                    for ring in polygon
                ]
                result.extend(rings)  # DataLens объединяет все кольца в один список
            return result
        else:
            return None
    except Exception as e:
        logger.debug(f"Ошибка при конвертации геометрии: {e}")
        return None

def calculate_area_km2(geom) -> float:
    try:
        shp = shape(geom)
        return max(round(shp.area * (111.0 ** 2), 2), 0.01)
    except:
        return 100.0


def fetch_osm_data(admin_level: str) -> Optional[Dict[Any, Any]]:
    query = f"""[out:json][timeout:600];
rel["ISO3166-1"="RU"]["admin_level"="2"];
map_to_area;
rel(area)["boundary"="administrative"]["admin_level"="{admin_level}"];
out geom;"""

    print(query)

    try:
        logger.info(f"📡 Запрос уровня {admin_level} к Overpass API...")
        response = requests.post(
            OVERPASS_URL,
            data=query.encode('utf-8'),
            headers={'Content-Type': 'text/plain; charset=utf-8'},
            timeout=600
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка запроса Overpass для уровня {admin_level}: {e}")
        return None


def process_and_save_to_db(geojson_data: Dict, admin_level: str):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        features = geojson_data.get('features', [])
        saved = 0
        for feature in features:
            props = feature.get('properties', {})
            geom = feature.get('geometry')
            if not geom or geom.get('type') not in ('Polygon', 'MultiPolygon'):
                continue

            polygon_coords = extract_geopolygon_coords(geom)
            if polygon_coords is None:
                continue

            shp = shape(geom)
            if not shp.is_valid:
                continue
            if shp.area > 0.01:
                shp = shp.simplify(0.001, preserve_topology=True)

            centroid = shp.centroid
            if centroid.is_valid:
                centroid_lat, centroid_lon = round(centroid.y, 6), round(centroid.x, 6)
            else:
                bounds = shp.bounds
                centroid_lat = round((bounds[1] + bounds[3]) / 2, 6)
                centroid_lon = round((bounds[0] + bounds[2]) / 2, 6)
            # pprint(props)
            name = props.get('tags').get('name:ru') or props.get('tags').props.get('name')
            if name:
                print(name)
            else:
                pprint(props)
            name_en = props.get('tags').get('name:en', '')
            population = 0
            pop_str = props.get('population', '')
            if isinstance(pop_str, str) and pop_str.isdigit():
                population = int(pop_str)
            elif isinstance(pop_str, (int, float)):
                population = int(pop_str)

            area_sq_km = calculate_area_km2(geom)

            insert_query = """
            INSERT INTO admin_boundaries 
            (osm_id, name, name_en, admin_level, admin_type, boundary_type, place_type,
             population, wikidata_id, wikipedia_url, polygon_coordinates,
             centroid_lat, centroid_lon, area_sq_km, polygon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                props.get('id'),
                str(name)[:250],
                str(name_en)[:250] if name_en else None,
                admin_level,
                get_admin_type(admin_level),
                props.get('boundary', 'administrative'),
                props.get('place', None),
                population,
                props.get('wikidata', None),
                props.get('wikipedia', None),
                json.dumps(geom, ensure_ascii=False),
                centroid_lat,
                centroid_lon,
                area_sq_km,
                json.dumps(polygon_coords, ensure_ascii=False)
            )
            try:
                cursor.execute(insert_query, data)
                saved += 1
            except Error as e:
                logger.warning(f"⚠️ Ошибка вставки объекта {props.get('id')}: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Успешно сохранено {saved} объектов уровня {admin_level}")

    except Error as e:
        logger.error(f"❌ Ошибка подключения к БД: {e}")
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {e}")


def main():
    print("🌍 Загрузка административных границ России в admin_boundaries")
    print("=" * 70)

    for level_name, admin_level in ADMIN_LEVELS.items():
        print(f"\n📥 Уровень: {level_name} (admin_level={admin_level})")
        raw_data = fetch_osm_data(admin_level)
        if not raw_data:
            logger.warning(f"⚠️ Пропуск уровня {admin_level} — нет данных")
            continue

        try:
            geojson_data = osm2geojson.json2geojson(raw_data)
        except Exception as e:
            logger.error(f"❌ Ошибка конвертации в GeoJSON: {e}")
            continue

        if not geojson_data.get('features'):
            logger.warning(f"⚠️ Нет объектов для уровня {admin_level}")
            continue

        process_and_save_to_db(geojson_data, admin_level)
        time.sleep(3)

    print("\n✅ Загрузка завершена. Данные сохранены в admin_boundaries.")


if __name__ == "__main__":
    main()