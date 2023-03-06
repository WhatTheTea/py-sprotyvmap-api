from dataclasses import dataclass, astuple
from cachetools import cached, LRUCache
import visicom_geocoder
from dotenv import load_dotenv
from os import getenv
import re

load_dotenv()
APIKEY = getenv("VISICOM")

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
    try:
        geocoder = visicom_geocoder.Geocoder(APIKEY)
        latlng = geocoder.geocode(location)
    except Exception as ex:
        if visicom_geocoder.GeocoderExceptions.NOT_FOUND in ex:
           latlng = geocode_regex_wrapper(location)
        else:
            print(ex)
            return None
    finally:
        return latlng

def geocode_regex_wrapper(geocoder:visicom_geocoder.Geocoder, location:str, **kwargs):
    # Якась область, м.\смт.\с. Якесь, вул. Якась, якийсь
    re_pattern = r"(\b\w+ область\b).*\b(м|смт?|с)\.\s*(\w+).*вул\.\s*(.*?)\s*,\s*(\d+)"
    re_result = re.search(re_pattern, location)
    if re_result:
        try:
            latlng = geocoder.geocode(re_result.string, **kwargs)
        except Exception as ex:
            print(ex)
    return latlng