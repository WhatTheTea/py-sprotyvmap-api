from data.Point import Point
from requests import get as http_get
from lxml import etree

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
        TODO
    Returns: 
        TODO
    """
    data = []
    for i in range(3):
        xpath = XPATH_DATA.format(district_id, point_id, i+1)
        raw = sprotyv_tree.xpath(xpath)
        data.append(cleanstr(raw))
    return Point(*data)

def district(district_id:int):
    """
    Повертає ім'я області та військкомати в ній\n
    Args:
        district_id (int): номер області (1..24)
    Returns:
        TODO
    """
    table = sprotyv_tree.xpath(XPATH_TABLE.format(district_id))[0].getchildren()
    district_name = "".join(sprotyv_tree.xpath(XPATH_DISTRICT.format(district_id))).strip()
    points_count = len(table) - 1
    points = [point(district_id, point_id) for point_id in range(1,points_count)]
    
    return {'district':district_name, 'points':points}

    
