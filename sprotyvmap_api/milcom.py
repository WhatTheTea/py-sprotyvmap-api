from dataclasses import dataclass, astuple
from cachetools import cached, LRUCache
import sprotyvmap_api.geocoder as geocoder
from dotenv import load_dotenv
from os import getenv
import re

# Отримання ключа 
load_dotenv()
APIKEY = getenv("VISICOM")
_geocoder = geocoder.Geocoder(APIKEY)
# Кеш для функції запиту до Visicom Data API
_cache = LRUCache(500)

@dataclass(frozen=True, eq=True)
class MilComRaw:
    """
    Об'єкт який зберігає необроблені дані про військкомати.\n
    """
    name:str
    info:str
    phones:str

    def __iter__(self):
        return iter(astuple(self))
@dataclass(eq=True)
class MilCom:    
    """
    Об'єкт який зберігає дані про військкомат та його координати.\n
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
def geocode_regex_wrapper(location:str, **kwargs) -> tuple:
    """
    Кешована функція отримання координат за назвою локації.\n
    Args:
        geocoder (visicom_geocoder.Geocoder): Visicom Geocoder API
        location (str): Локація для знаходження
        **kwargs: див. geocoder.geocode
    Returns:
        Tuple[int,int]: Координати локації
    """
    # Якась область, м.\смт.\с. Якесь, вул. Якась, якийсь
    re_district_pattern = r"[А-Яа-яіІ-]+ (обл\.|область)"
    re_town_pattern = r"((м\.|смт\.|с\.|смт|пгт\.)\s*[А-Яа-яіІ-]+)((.*\d[а-я]{1})|(.*\d))"
    district = re_district.group() if (re_district := re.search(re_district_pattern, location)) else ''
    town = re_town.group() if (re_town := re.search(re_town_pattern, location)) else ''
    try:
        re_location = district + " " + town if town.strip() != "" else location
        return _geocoder.geocode(re_location, **kwargs)
    except Exception as ex:
        print(ex, f"pre regex: {location}")
        return