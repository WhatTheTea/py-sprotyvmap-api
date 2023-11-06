import sprotyvmap_api.data.preprocessing as dp
from sprotyvmap_api.data.Point import Point
from typing import List
import json

def raw_data():
    milcoms_raw = dp.all_districts()
    if milcoms_raw:
        data = json.dumps(milcoms_raw)
        return data
    

def point(district_id:int, point_id:int):
    point = dp.point(district_id, point_id).asdict()
    if point:
        data = json.dumps(point)
        return data

def all_districts():
    return districts_generator()


def district(district_id:int):
    """
    Отримує всі координати військкоматів в області під номером district_id

    Args:
        district_id (int): номер області (1..24)
    Returns:
        flask.Response : HTTP відповідь з JSON даними про військкомати в окремій області
    """
    name, points = dp.district(district_id)
    data = points_generator(points)
    if data:
        result = "{"
        result += f'"{name}":'
        result += json.dumps(data)
        result += '}'
        return result

def districts_generator():
        """
        Генерує дані про військкомати у форматі:
        { "district":[...], "other":[...] }
        
        Returns: 
            Generator[str, None, None] : Генератор потокових даних про всі військкомати України
        """
        yield '{'
        # Отримання "сирих" військкоматів
        districts = list(dp.all_districts().items())

        for i in range(len(districts)):
            # Розпаковка області
            name, milcoms_raw = districts[i]

            yield f'"{name}":'
            milcoms = points_generator(milcoms_raw)
            yield json.dumps(milcoms)
            if i < len(districts)-1:
                yield ","
        yield '}'

def points_generator(points:List[Point]) -> List[dict]:
    """
    Обробляє спарсені військкомати та фільтрує від пустих словників

    Args:
        milcoms_raw (List[MilComRaw]) : "сира" інформація про військкомати для обробки
    Returns:
        List[dict] : Представлення об'єктів MilCom у вигляді словників
    """
    return [point.asdict() for point in points if point]

