from typing import Tuple
from enum import Enum
import requests

class GeocoderExceptions(Enum):
    BAD_API_KEY = -1
    REQUEST_NOT_OK = -2
    NOT_FOUND = -3

class GeocoderException(Exception):
    def __init__(self, text : str, type : GeocoderExceptions, *args) -> None:
        super().__init__([text, type, *args])

"""
Із вебсайту Visicom Geocoding API:
    https://api.visicom.ua/data-api/5.0/[lang]/geocode[.format]?
    [categories|ci]
    [&text|t]
    [&word_text|wt]
    [&near|n|intersect|i|contains|co]
    [&radius|r]
    [&limit|l]
    [&country|c]
    [&boost_country|bc]
    [&zoom]
    [&key]
    [&callback]

    lang	
        Мова запиту і відповіді. Одна з (ru, uk, en).
    format	
        Формат даних, що повертаються (json, csv).
    !categories	
        Список ідентифікаторів категорій через «,» в яких буде виконуватися пошук об'єктів.
    !categories_exclude	
        Список ідентифікаторів категорій через «,» котрі будуть виключені з результатів пошуку.
    !word_text
        Слова, які повинні зустрічатися в описі об'єкта. Приклад: word_text=Київ. В пошук не потраплять Київський, Київська і т.д.
    !near
        Ідентифікатор об'єкта або геометрія в форматі WKT з кількістю вершин не більше 250. 
        Для точок можливий спрощений запис у вигляді lng,lat. 
        Відстань до заданої геометрії буде враховуватися при формуванні результату. 
        Приклад: near=POIA1KIGKN, n=30.5113,50.4550.
    !radius
        Радіус в метрах навколо місця розташування, яке задано параметром near.
    !order	
        Параметр вказує на тип сортування об'єктів у відповіді. 
        Може приймати значення relevance (сортування за релевантністю об'єктів для даного запиту), 
        distance (сортування за віддаленістю від місця, вказаного параметром near). За замовченням - значення relevance.
    !intersect
        Ідентифікатор об'єкта або геометрія в форматі WKT з кількістю вершин не більше 250. 
        Для точок можливий спрощений запис у вигляді lng,lat. 
        Запит повертає об'єкти, геометрія яких перетинається з геометрією, описаною даними параметром.
    !contains	
        Ідентифікатор об'єкта або геометрія в форматі WKT з кількістю вершин не більше 250. 
        Для точок можливий спрощений запис у вигляді lng,lat. Запит повертає об'єкти, 
        геометрія яких знаходиться всередині геометрії, описаної даним параметром.
    !zoom	
        Масштаб карти по специфікації TMS. Чим менше масштаб, тим менше враховуються координати, 
        зазначені параметром near при розрахунку релевантності об'єктів.
    !limit
        Максимальна кількість об'єктів, що повертаються. Максимум 250.
    !country	
        Код країни.
    !boost_country	
        Код країни. Якщо не вказаний параметр country, 
        то об'єкти в зазначеній цим параметром країні мають більший пріоритет.
"""
class Geocoder:
    """
    Неповна реалізація geocoding API від Visicom.
    """
    _apikey: str
    _allowedArgs = {'lang', 'key', 'format', 'text', 'limit'}

    def __init__(self, apikey:str) -> None:
        self._apikey = apikey

    def geocode(self, location:str, **kwargs) -> Tuple[int,int]:
        """
Функція пошуку координат місця даному в `location`.\n
Args:
    location (str):
        Текст для геокодування
    **kwargs:
        lang (str):
            Мова запиту і відповіді. Одна з (ru, uk, en).
                default: uk
        format (str):
            Формат даних, що повертаються (json, csv).
                default: json
Returns: 
    Tuple[int,int]: Координати шуканої локації (latitude, longitude)
        """
        # Запит
        request_str = self.build_request(location, **kwargs)
        response = requests.get(request_str)
        # 
        if response.text == "{'status': 'Unauthorized'}" or response.status_code == 401:
            raise GeocoderException(f"Не вдалося отримати доступ до сервісу геокодування. Перевірте ключ API", GeocoderExceptions.BAD_API_KEY)
        
        if not response.ok:
            raise GeocoderException(f"Запит до сервісу геокодування не був успішим. Помилка {response.status_code} {response.reason}", GeocoderExceptions.REQUEST_NOT_OK)
        
        if response.text == "{}":
            raise GeocoderException(f"Не вдалося знайти координати за адресою: {location}", GeocoderExceptions.NOT_FOUND)
        
        request_json = response.json()
        point = request_json["geo_centroid"]['coordinates']
        coords = point[1], point[0]
        return coords
    
    def build_request(self, location : str, **kwargs):
        preset_kwargs = {
                "format" : "json",
                "key" : self._apikey,
                "text" : location,
                "limit" : 1
            }
        default_kwargs = {"lang" : "uk"}
        kwargs = {**default_kwargs, **kwargs, **preset_kwargs} # Захист від підміни важливих аргументів
        # Конструювання HTTP запиту
        request_str = f'https://api.visicom.ua/data-api/5.0/{kwargs.pop("lang")}/geocode.{kwargs.pop("format")}?'

        for k,v in kwargs.items():
            if k in self._allowedArgs:
                v = str(v).replace('&','').replace('?','')
                request_str += f'&{k}={v}'

        return request_str