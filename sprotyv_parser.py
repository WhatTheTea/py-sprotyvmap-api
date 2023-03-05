from typing import Dict,List,Tuple
from lxml import etree
from requests import get as http_get
from sprotyv_milcom import MilComRaw

# Завантаження дерева сайту
sprotyv_html = http_get("https://sprotyv.in.ua/").text
sprotyv_tree = etree.HTML(sprotyv_html)
# TODO: Error handling

# XPath потрібних даних
# .format: 1 - область, 2 - військомат, 3 - стовпець
xpath_data = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody/tr[{}]/td[{}]/text()" 
xpath_table = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody/text()"
xpath_district = "/html/body/div/section[2]/div/div[{}]/div/div[1]/span/span[1]/text()"

def milcom_raw(district_id: int, milcom_id: int) -> MilComRaw:
    """
    Парсить адресу та інфо воєнкомату з сайту за номером області та номером воєнкомата.\n
    Номер воєнкомата є відносним кожної окремої області.\n
    Args:
        district_id (int): номер області (1..24)
        milcom_id (int): номер воєнкомату (1..n)
    Returns: 
        MilComRaw: "сирі" дані про воєнкомат з адресою замість координат.
    """
    name = "".join(sprotyv_tree.xpath(xpath_data.format(district_id, milcom_id, 1))).strip()
    info = "".join(sprotyv_tree.xpath(xpath_data.format(district_id, milcom_id, 2))).strip()
    phones = "".join(sprotyv_tree.xpath(xpath_data.format(district_id, milcom_id, 3))).strip()
    return MilComRaw(name, info, phones)

def district_raw(district_id:int) -> Tuple[str, List[MilComRaw]]:
    """
    Повертає ім'я області та воєнкомати в ній\n
    Args:
        district_id (int): номер області (1..24)
    Returns:
        Tuple[str, List[MilComRaw]]: кортеж з імені області та списку "сирих" воєнкоматів
    """
    table = sprotyv_tree.xpath(xpath_table.format(district_id))
    district_name = "".join(sprotyv_tree.xpath(xpath_district.format(district_id))).strip()
    milcoms_count = len(table) - 1
    milcoms_raw = [milcom_raw(district_id, milcom_id) for milcom_id in range(1,milcoms_count)]
    
    return (district_name, milcoms_raw)

def districts_raw() -> Dict[str, List[MilComRaw]]:
    """
    Повертає список спарсених адрес воєнкоматів розділених по областям\n
    Returns:
        Dict[str, List[MilComRaw]]: словник ім'я області : список "сирих" воєнкоматів
    """
    districts_raw = dict()
    for district_id in range(1,24+1):
        # DistrictTuple: 0 - name; 1 - milcoms
        district_tuple = district_raw(district_id)
        districts_raw[district_tuple[0]] = district_tuple[1]
    return districts_raw

