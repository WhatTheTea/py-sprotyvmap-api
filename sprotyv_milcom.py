from dataclasses import dataclass, astuple
import visicom_geocoder
from dotenv import load_dotenv
from os import getenv
import re

load_dotenv()
APIKEY = getenv("VISICOM")
"""
MilCom - military commissariat (військомат)
"""
@dataclass
class MilComRaw:
    """
    Об'єкт який зберігає необроблені дані про воєнкомати.\n
    """
    name:str
    info:str
    phones:str

    def __iter__(self):
        return iter(astuple(self))
@dataclass
class MilCom:    
    """
    Об'єкт який зберігає дані про воєнкомат та його координати.\n
    ! При створенні цього об'єкту відбувається звернення до API\n
    ! Це може вплинути на швидкодію
    """
    name:str
    latlng:tuple
    info:str

    def __init__(self, name:str, info:str, phones:str):
        geocoder = visicom_geocoder.Geocoder(APIKEY)
        response = geocoder.geocode(info)
        if not response:
            re_pattern = r"(\b\w+ область\b).*\b(м|смт?|с)\.\s*(\w+).*вул\.\s*(.*?)\s*,\s*(\d+)"
            re_result = re.search(re_pattern, info)
            if re_result:
                response = geocoder.geocode(re_result.string)
        if response:
            self.info = phones
            self.latlng = response
            self.name = name
    
    def __iter__(self):
        return iter(astuple(self))