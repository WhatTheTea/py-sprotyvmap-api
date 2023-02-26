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
xpath_tbody = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody/text()"
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

def milcoms_raw() -> list:
    """
    Повертає список спарсених адрес воєнкоматів
    """
    milcoms_raw = []
    for district_id in range(1,24+1):
        tbody = sprotyv_tree.xpath(xpath_tbody.format(district_id))
        milcoms_count = len(tbody) - 1
        for milcom_id in range(1,milcoms_count):
            milcom = milcom_raw(district_id, milcom_id)
            milcoms_raw.append(milcom)
    return milcoms_raw
