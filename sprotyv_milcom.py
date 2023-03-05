from dataclasses import dataclass, astuple
from cachetools import cached, LRUCache
import visicom_geocoder
from dotenv import load_dotenv
from os import getenv
import re

load_dotenv()
APIKEY = getenv("VISICOM")

_cache = LRUCache(500)
"""
MilCom - military commissariat (військомат)
"""
@dataclass
class MilComRaw:
    """
    Об'єкт який зберігає необроблені дані про воєнкомати.\n
    """
    name:str
    info:str
    phones:str

    def __iter__(self):
        return iter(astuple(self))
@dataclass
class MilCom:    
    """
    Об'єкт який зберігає дані про воєнкомат та його координати.\n
    ! Створення цього об'єкту є дорогим, але результат дорогої функції кешується
    """
    name:str
    latlng:tuple
    info:str

    def __init__(self, name:str, info:str, phones:str):
        latlng = _latlng_(info)
        if latlng:
            self.info = phones
            self.latlng = latlng
            self.name = name

    def __iter__(self):
        return iter(astuple(self))
    
@cached(_cache)
def _latlng_(location:str):
    """
    Кешована функція отримання координат за назвою локації.\n
    Додатково шукає назву міста, вулиці, будинку у разі некоректного location
    Args:
        location (str): Локація для знаходження
    Returns:
        Tuple[int,int]: Координати локації
    """
    geocoder = visicom_geocoder.Geocoder(APIKEY)
    latlng = geocoder.geocode(location)
    if not latlng:
        re_pattern = r"(\b\w+ область\b).*\b(м|смт?|с)\.\s*(\w+).*вул\.\s*(.*?)\s*,\s*(\d+)"
        re_result = re.search(re_pattern, location)
        if re_result:
            latlng = geocoder.geocode(re_result.string)
    return latlng