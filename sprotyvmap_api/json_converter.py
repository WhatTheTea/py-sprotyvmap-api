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


def district(district_id:int):
    """
    Отримує всі координати військкоматів в області під номером district_id

    Args:
        district_id (int): номер області (1..24)
    Returns:
        flask.Response : HTTP відповідь з JSON даними про військкомати в окремій області
    """
    district = dp.district(district_id)
    points = [point.asdict() for point in district['points'] if point]
    return json.dumps({
        'district': district['district'],
        'points': points
        })

def all_districts():
    data = [data.append(district(i)) for i in range(1,24+1)]
    return data
        