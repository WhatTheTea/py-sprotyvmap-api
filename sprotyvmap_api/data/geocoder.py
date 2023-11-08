from typing import Tuple
import requests

class GeocoderException(Exception):
    message : str
    status : int
    def __init__(self, message, status):
        super().__init__(message)
        self.status = status

    def __str__(self):
        return f"{self.status} : {self.message}"

class Geocoder:
    """
    Неповна реалізація geocoding API від Visicom.
    """
    def __init__(self, apikey:str) -> None:
        self._apikey = apikey

    _allowedArgs = {'lang', 'key', 'format', 'text', 'limit'}

    def set_apikey(self, key : str):
        self._apikey = key
        
    def geocode(self, location:str, **kwargs) -> Tuple[int,int]:
        """
Метод пошуку координат місця даному в `location`.\n
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
            raise GeocoderException(f"Не вдалося отримати доступ до сервісу геокодування. Перевірте ключ API", 401)
        
        if not response.ok:
            raise GeocoderException(f"Запит до сервісу геокодування не був успішим. Помилка: {response.reason}", response.status_code)
        
        if response.text == "{}":
            raise GeocoderException(f"Не вдалося знайти координати за адресою: {location}", 404)
        
        response_json = response.json()
        point = response_json["geo_centroid"]['coordinates']
        coords = point[1], point[0]
        return coords
    
    def build_request(self, location : str, **kwargs):
        """
Метод створення запиту для пошуку координат місця даному в `location`.\n
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
    str : Рядок запиту до стороннього API
        """
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

        for key,value in kwargs.items():
            if key in self._allowedArgs:
                value = str(value).replace('&','').replace('?','')
                request_str += f'&{key}={value}'

        return request_str