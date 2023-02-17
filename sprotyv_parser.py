from collections import namedtuple
from lxml import etree
import requests

# Структура з даними з сайту
milcom_raw = namedtuple('MilComRaw', 'name info phones')
# Завантаження дерева сайту
sprotyv_html = requests.get("https://sprotyv.in.ua/")
sprotyv_tree = etree.HTML(sprotyv_html)
# TODO: Error handling

for obl in range(0,24):
