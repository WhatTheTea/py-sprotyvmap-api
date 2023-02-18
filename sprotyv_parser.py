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

def get_milcom_raw(obl: int, milcom: int):
    name = "".join(sprotyv_tree.xpath(xpath.format(obl, milcom, 1))).strip()
    info = "".join(sprotyv_tree.xpath(xpath.format(obl, milcom, 2))).strip()
    phones = "".join(sprotyv_tree.xpath(xpath.format(obl, milcom, 3))).strip()
    return milcom_raw(name, info, phones)

def get_milcoms_raw() -> list:
    # Парсинг даних з сайту
    milcoms_raw = []
    for i_obl in range(1,24+1):
        tbody = sprotyv_tree.xpath(f"/html/body/div/section[2]/div/div[{i_obl}]/div/div[2]/div/div/table/tbody/text()")
        tlen = len(tbody) - 1
        for i_milcom in range(1,tlen): #TODO: N of milcoms
            milcom = get_milcom_raw(i_obl, i_milcom)
            milcoms_raw.append(milcom)
    return milcoms_raw
