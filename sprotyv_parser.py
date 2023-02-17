from collections import namedtuple
from lxml import etree
import requests

# Структура з даними з сайту 
# MilCom - military commissariat (військомат)
milcom_raw = namedtuple('MilComRaw', 'name info phones')
# Завантаження дерева сайту
sprotyv_html = requests.get("https://sprotyv.in.ua/").text
sprotyv_tree = etree.HTML(sprotyv_html)
# TODO: Error handling

# XPath потрібних даних
# .format: 1 - область, 2 - військомат, 3 - стовпець
xpath = "/html/body/div/section[2]/div/div[{}]/div/div[2]/div/div/table/tbody/tr[{}]/td[{}]/text()" 

def get_milcoms() -> list:
    # Парсинг даних з сайту
    milcoms_raw = []
    for i_obl in range(1,24+1):
        for i_milcom in range(1,2+1): #TODO: N of milcoms
            name = sprotyv_tree.xpath(xpath.format(i_obl, i_milcom, 1))[0]
            info = sprotyv_tree.xpath(xpath.format(i_obl, i_milcom, 2))[0]
            phones = sprotyv_tree.xpath(xpath.format(i_obl, i_milcom, 3))[0]
            milcoms_raw.append(milcom_raw(name, info, phones))
    return milcoms_raw

