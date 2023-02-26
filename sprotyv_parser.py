from typing import *
from lxml import etree
from requests import get as http_get
import sprotyv_milcom

# Завантаження дерева сайту
sprotyv_html = http_get("https://sprotyv.in.ua/").text
sprotyv_tree = etree.HTML(sprotyv_html)
# TODO: Error handling

# XPath потрібних даних
# .format: 1 - область, 2 - військомат, 3 - стовпець
xpath_data = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody/tr[{}]/td[{}]/text()" 
xpath_table = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody/text()"
xpath_district = "/html/body/div/section[2]/div/div[{}]/div/div[1]/span/span[1]/text()"

def milcom_raw(district: int, milcom: int) -> sprotyv_milcom.MilComRaw:
    """
    Парсить адресу та інфо воєнкомату з сайту за номером області та номером воєнкомата.\n
    Номер воєнкомата є відносним кожної окремої області.
    """
    name = "".join(sprotyv_tree.xpath(xpath_data.format(district, milcom, 1))).strip()
    info = "".join(sprotyv_tree.xpath(xpath_data.format(district, milcom, 2))).strip()
    phones = "".join(sprotyv_tree.xpath(xpath_data.format(district, milcom, 3))).strip()
    return sprotyv_milcom.MilComRaw(name, info, phones)

def district_raw(district_id:int) -> Tuple[str, list]:
    """
    Поветрає ім'я області та воєнкомати в ній
    """
    table = sprotyv_tree.xpath(xpath_table.format(district_id))
    district_name = "".join(sprotyv_tree.xpath(xpath_district.format(district_id))).strip()
    milcoms_count = len(table) - 1
    milcoms_raw = [milcom_raw(district_id, milcom_id) for milcom_id in range(1,milcoms_count)]
    
    return (district_name, milcoms_raw)

def districts_raw() -> Dict[str, List[sprotyv_milcom.MilComRaw]]:
    """
    Повертає список спарсених адрес воєнкоматів розділених по областях
    """
    districts_raw = dict()
    for district_id in range(1,24+1):
        # DistrictTuple: 0 - name; 1 - milcoms
        district_tuple = district_raw(district_id)
        districts_raw[district_tuple[0]] = district_tuple[1]
    return districts_raw

