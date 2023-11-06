import sprotyvmap_api.data.data_preprocessing as dp
from typing import List
import json

def raw_data():
    milcoms_raw = dp.all_districts()
    if milcoms_raw:
        data = json.dumps(milcoms_raw)
        return data
    

def milcom(district_id:int, milcom_id:int):
    milcom_raw = dp.milcom(district_id, milcom_id)
    milcom = dp.MilCom(*milcom_raw).__dict__
    if milcom:
        data = json.dumps(milcom)
        return data

def all_districts():
    return generate_districts()


def district(district_id:int):
    """
    Отримує всі координати військкоматів в області під номером district_id

    Args:
        district_id (int): номер області (1..24)
    Returns:
        flask.Response : HTTP відповідь з JSON даними про військкомати в окремій області
    """
    name, milcoms_raw = dp.district(district_id)
    data = generate_milcoms(milcoms_raw)
    if data:
        result = "{"
        result += f'"{name}":'
        result += json.dumps(data)
        result += '}'
        return result

def generate_districts():
        """
        Генерує дані про військкомати у форматі:
        { "district":[...], "other":[...] }
        
        Returns: 
            Generator[str, None, None] : Генератор потокових даних про всі військкомати України
        """
        yield '{'
        # Отримання "сирих" військкоматів
        districts = list(dp.all_districts().items())

        for i in range(len(districts)):
            # Розпаковка області
            name, milcoms_raw = districts[i]

            yield f'"{name}":'
            milcoms = generate_milcoms(milcoms_raw)
            yield json.dumps(milcoms)
            if i < len(districts)-1:
                yield ","
        yield '}'

def generate_milcoms(milcoms_raw:List[dp.MilComRaw]) -> List[dict]:
    """
    Обробляє спарсені військкомати та фільтрує від пустих словників

    Args:
        milcoms_raw (List[MilComRaw]) : "сира" інформація про військкомати для обробки
    Returns:
        List[dict] : Представлення об'єктів MilCom у вигляді словників
    """
    return [milcom for milcom_raw in milcoms_raw if (milcom := dp.MilCom(*milcom_raw).__dict__)]

