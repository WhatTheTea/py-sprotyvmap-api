import sprotyvmap_api.geocoder as geocoder

from dotenv import load_dotenv
from os import getenv

from cachetools import cached, LRUCache
from requests import get as http_get
from typing import Dict,List,Tuple
from lxml import etree
import re

# Завантаження дерева сайту
sprotyv_html = http_get("https://sprotyv.in.ua/").text
sprotyv_tree = etree.HTML(sprotyv_html)

# XPath потрібних даних
# .format: 1 - область, 2 - військомат, 3 - стовпець
XPATH_DATA = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody/tr[{}]/td[{}]/text()" 
XPATH_TABLE = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody"
XPATH_DISTRICT = "/html/body/div/section[2]/div/div[{}]/div/div[1]/span/span[1]/text()"

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
# ? use re
def cleanstr(obj):
    return "".join(obj).strip().replace('\n', '').replace('\\n','')

def milcom(district_id: int, milcom_id: int) -> Point:
    """
    Парсить адресу та інфо військкомату з сайту за номером області та номером військкомата.\n
    Номер військкомата є відносним кожної окремої області.\n
    Args:
        district_id (int): номер області (1..24)
        milcom_id (int): номер військкомату (1..n)
    Returns: 
        MilComRaw: "сирі" дані про військкомат з адресою замість координат.
    """
    data = []
    for i in range(3):
        xpath = XPATH_DATA.format(district_id, milcom_id, i+1)
        raw = sprotyv_tree.xpath(xpath)
        data.append(cleanstr(raw))
    return Point(*data)

def district(district_id:int) -> Tuple[str, List[Point]]:
    """
    Повертає ім'я області та військкомати в ній\n
    Args:
        district_id (int): номер області (1..24)
    Returns:
        Tuple[str, List[MilComRaw]]: кортеж з імені області та списку "сирих" військкоматів
    """
    table = sprotyv_tree.xpath(XPATH_TABLE.format(district_id))[0].getchildren()
    district_name = "".join(sprotyv_tree.xpath(XPATH_DISTRICT.format(district_id))).strip()
    milcoms_count = len(table) - 1
    milcoms_raw = [milcom(district_id, milcom_id) for milcom_id in range(1,milcoms_count)]
    
    return (district_name, milcoms_raw)

def all_districts() -> Dict[str, List[Point]]:
    """
    Повертає список спарсених адрес військкоматів розділених по областям\n
    Returns:
        Dict[str, List[MilComRaw]]: словник ім'я області : список "сирих" військкоматів
    """
    districts_raw = dict()
    for district_id in range(1,24+1):
        # DistrictTuple: 0 - name; 1 - milcoms
        district_tuple = district(district_id)
        districts_raw[district_tuple[0]] = district_tuple[1]
    return districts_raw

    
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