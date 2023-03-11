from dataclasses import dataclass, astuple
from cachetools import cached, LRUCache
import visicom_geocoder
from dotenv import load_dotenv
from os import getenv
import re

# Отримання ключа 
load_dotenv()
APIKEY = getenv("VISICOM")
# Кеш для функції запиту до Visicom Data API
_cache = LRUCache(500)

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
        latlng = geocode_regex_wrapper(info)
        if latlng:
            self.info = phones
            self.latlng = latlng
            self.name = name

    def __iter__(self):
        return iter(astuple(self))
    
@cached(_cache)
def geocode_regex_wrapper(location:str, **kwargs):
    """
    Кешована функція отримання координат за назвою локації.\n
    Args:
        geocoder (visicom_geocoder.Geocoder): Visicom Geocoder API
        location (str): Локація для знаходження
        **kwargs: див. geocoder.geocode
    Returns:
        Tuple[int,int]: Координати локації
    """
    geocoder = visicom_geocoder.Geocoder(APIKEY)
    # Якась область, м.\смт.\с. Якесь, вул. Якась, якийсь
    re_distric_pattern = r"[А-Яа-яіІ-]+ (обл\.|область)"
    re_town_pattern = r"((м\.|смт\.|с\.|смт|пгт\.)\s*[А-Яа-яіІ-]+)((.*\d[а-я]{1})|(.*\d))"
    district = dre.group() if (dre := re.search(re_distric_pattern, location)) else ''
    town = tre.group() if (tre := re.search(re_town_pattern, location)) else ''
    try:
        loc = district + " " + town if town.strip() != "" else location
        return geocoder.geocode(loc, **kwargs)
    except Exception as ex:
        print(ex, f"pre regex: {location}")
        return