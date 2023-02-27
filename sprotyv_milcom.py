from dataclasses import dataclass, astuple
import geocoder
from dotenv import load_dotenv
from os import getenv

load_dotenv()
GMAPSKEY = getenv("GMAPSKEY")
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
    ! При створенні цього об'єкту відбувається звернення до Google Maps API\n
    ! Це може вплинути на швидкодію
    """
    name:str
    latlng:tuple
    info:str

    def __init__(self, name:str, info:str, phones:str):
        response = geocoder.google(info, key=GMAPSKEY) # TODO: Error handling
        if(response):
            self.info = phones
            self.latlng = response.latlng
            self.name = name
        print(f"Адресу {info} не було знайдено")
    
    def __iter__(self):
        return iter(astuple(self))

def get(name:str, info:str, phones:str) -> MilCom:
    return MilCom(name, info, phones)