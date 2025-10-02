# polygon_processor.py
import requests
import json
import ast
from shapely.geometry import shape


class PolygonProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.insert_query = """
        INSERT INTO points (
            id, name, polygon,
            startDateTime, endDateTime, nameSpace, uuid, airspaceType,
            schedule, lowerLimit, upperLimit, meta, isActive,
            lowerLimitValue, upperLimitValue, lowerLimitUnits, lowerLimitVerticalReference,
            upperLimitUnits, upperLimitVerticalReference
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    def parse_polygon_string(self, polygon_str):
        """Преобразование строки полигона в GeoJSON-формат"""
        try:
            return json.loads(polygon_str)
        except json.JSONDecodeError:
            try:
                return ast.literal_eval(polygon_str)
            except (ValueError, SyntaxError):
                raise ValueError(f"Не удалось распарсить строку полигона: {polygon_str}")

    def swap_coordinates(self, features):
        """Обмен координат в геообъектах"""
        for feature in features:
            coordinates = feature['geometry']['coordinates']
            geom_type = feature['geometry']['type']

            if geom_type == 'MultiPolygon':
                for polygon in coordinates:
                    for ring in polygon:
                        for point in ring:
                            point[0], point[1] = point[1], point[0]
            elif geom_type == 'Polygon':
                for ring in coordinates:
                    for point in ring:
                        point[0], point[1] = point[1], point[0]
            elif geom_type == 'LineString':
                for point in coordinates:
                    point[0], point[1] = point[1], point[0]
            elif geom_type == 'Point':
                coordinates[0], coordinates[1] = coordinates[1], coordinates[0]

    def get_data(self, lat, lng):
        """Получение данных о полигонах по координатам"""
        try:
            url = "https://skyarc.ru/features/atpoint"
            params = {'lat': lat, 'lng': lng}
            print(url, params)
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе данных: {e}")
            return None

    def add_date_to_points(self, data):
        """Добавление данных о точках в базу данных"""
        self.swap_coordinates(data['features'])

        connection = self.db_manager.get_connection()
        if not connection:
            print("Не удалось получить соединение с базой данных")
            return

        cursor = connection.cursor()

        try:
            feature_ids = [feature.get('_id', '') for feature in data.get('features', [])]
            if not feature_ids:
                return

            format_strings = ','.join(['%s'] * len(feature_ids))
            if not self.db_manager.safe_execute(cursor, f"SELECT id FROM points WHERE id IN ({format_strings})",
                                                tuple(feature_ids)):
                return

            existing_ids = {row[0] for row in cursor.fetchall()}
            insert_data = []

            for feature in data.get('features', []):
                _id = feature.get('_id', '')
                if _id in existing_ids:
                    continue

                geometry = feature.get('geometry', {})
                coordinates = geometry.get('coordinates', [])
                properties = feature.get('properties', {})

                name = properties.get('name', '')
                startDateTime = properties.get('startDateTime')
                endDateTime = properties.get('endDateTime')
                nameSpace = properties.get('nameSpace')
                uuid = properties.get('uuid')
                airspaceType = properties.get('airspaceType')
                schedule_data = properties.get('schedule')
                schedule = json.dumps(schedule_data) if schedule_data else None
                meta = json.dumps(properties.get('meta', {})) if properties.get('meta') else None
                isActive = properties.get('isActive')

                lowerLimit = properties.get('lowerLimit', {})
                upperLimit = properties.get('upperLimit', {})

                lowerLimitValue = lowerLimit.get('value')
                lowerLimitUnits = lowerLimit.get('units')
                lowerLimitVerticalReference = lowerLimit.get('verticalReference')
                upperLimitValue = upperLimit.get('value')
                upperLimitUnits = upperLimit.get('units')
                upperLimitVerticalReference = upperLimit.get('verticalReference')

                lowerLimit_json = json.dumps(lowerLimit) if lowerLimit else None
                upperLimit_json = json.dumps(upperLimit) if upperLimit else None

                insert_data.append((
                    _id, name, str(coordinates[0]), startDateTime, endDateTime,
                    nameSpace, uuid, airspaceType, schedule, lowerLimit_json,
                    upperLimit_json, meta, isActive, lowerLimitValue,
                    upperLimitValue, lowerLimitUnits, lowerLimitVerticalReference,
                    upperLimitUnits, upperLimitVerticalReference
                ))

            if insert_data:
                if self.db_manager.safe_executemany(cursor, self.insert_query, insert_data):
                    connection.commit()
                    print(f"Добавлено {len(insert_data)} новых записей в таблицу points")
                else:
                    print("Не удалось вставить данные в таблицу points")

        finally:
            cursor.close()
            connection.close()

    def calculate_intersections(self):
        """Вычисление пересечений между точками и регионами"""
        connection = self.db_manager.get_connection()
        if not connection:
            print("Не удалось получить соединение с базой данных")
            return

        cursor = connection.cursor()

        try:
            if not self.db_manager.safe_execute(cursor, "SELECT id, polygon FROM points"):
                return
            points = cursor.fetchall()

            if not self.db_manager.safe_execute(cursor, "SELECT id, polygon FROM regions"):
                return
            regions = cursor.fetchall()

            region_polygons = []
            for region in regions:
                try:
                    poly_data = self.parse_polygon_string(region[1])
                    polygon = shape({"type": "Polygon", "coordinates": poly_data})
                    region_polygons.append({
                        'id': region[0],
                        'polygon': polygon
                    })
                except Exception as e:
                    print(f"Ошибка обработки региона {region[0]}: {str(e)}")

            for point in points:
                try:
                    point_data = self.parse_polygon_string(point[1])
                    point_polygon = shape({"type": "Polygon", "coordinates": point_data})

                    for region in region_polygons:
                        if point_polygon.intersects(region['polygon']):
                            insert_query = """
                            INSERT INTO point_region_intersections (point_id, region_id)
                            VALUES (%s, %s)
                            """
                            if self.db_manager.safe_execute(cursor, insert_query, (str(point[0]), region['id'])):
                                connection.commit()
                except Exception as e:
                    print(f"Ошибка обработки точки {point[0]}: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def set_points_polygon(self):
        """Обработка полигонов для всей территории России"""
        min_lat, max_lat = 41, 82
        min_lon, max_lon = 10, 160
        step = 40

        for lat in range(int(min_lat / step), int(max_lat / step) + 1):
            for lon in range(int(min_lon / step), int(max_lon / step) + 1):
                current_lat = lat * step
                current_lon = lon * step
                print(f"Обрабатываем координаты: {current_lat:.1f}, {current_lon:.1f}")

                data = self.get_data(current_lat, current_lon)
                if data:
                    self.add_date_to_points(data)