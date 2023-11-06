from data.Point import Point
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

# ? use re
def cleanstr(obj):
    return "".join(obj).strip().replace('\n', '').replace('\\n','')

def point(district_id: int, point_id: int) -> Point:
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
        xpath = XPATH_DATA.format(district_id, point_id, i+1)
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
    points_count = len(table) - 1
    points = [point(district_id, milcom_id) for milcom_id in range(1,points_count)]
    
    return (district_name, points)

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

    
