from typing import NamedTuple
import geocoder
"""
MilCom - military commissariat (військомат)
"""
class MilComRaw(NamedTuple):
    """
    Клас який зберігає необроблені дані про воєнкомати.\n
    """
    name:str
    info:str
    phones:str
class MilCom(NamedTuple):    
    """
    Клас який зберігає дані про воєнкомат та його координати.\n
    """
    name:str
    latlng:tuple
    info:str

def get(name:str, info:str, phones:str) -> MilCom:
    """
    Повертає клас даних воєнкомата з отриманими координатами від geocodefarm.
    """
    response = geocoder.geocodefarm(info) # TODO: Error handling
    if(response):
        latlng = response.latlng
        return MilCom(name, latlng, phones)
    print(f"Адресу {info} не було знайдено")
    return None