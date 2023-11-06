import sprotyvmap_api.data.geocoder as geocoder
from cachetools import cached, LRUCache
from dotenv import load_dotenv
from typing import Tuple
from os import getenv
import re
# Отримання ключа 
load_dotenv()
APIKEY = getenv("VISICOM")
_geocoder = geocoder.Geocoder(APIKEY)
# Кеш для функції запиту до Geocoder API
_cache = LRUCache(500)

class Point():
    def __init__(self, name : str, location : str, info : str):
        self.name = name
        self.location = location
        self._latlng : Tuple[float, float] = None
        self.info = info

    @property
    def latlng(self) -> Tuple[float,float]:
        self._latlng = self._latlng if self._latlng else geocode_regex_wrapper(self.location)
        return self._latlng

    def asdict(self):
        return {
            'name' : self.name,
            'location' : self.location,
            'latlng' : self.latlng,
            'info' : self.info
        }
    
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