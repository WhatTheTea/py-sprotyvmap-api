import flask
import sprotyv_parser
import json
from typing import Dict, List
from sprotyv_milcom import MilCom, MilComRaw

app = flask.Flask(__name__)

@app.route("/get/districts/raw")
def get_raw_milcoms():
    """
    Отримує всі адреси військкоматів України + контактні дані

    Returns:
        flask.Response : HTTP відповідь з JSON даними про всі військкомати України
    """
    milcoms_raw = sprotyv_parser.districts_raw()
    if milcoms_raw:
        response = flask.jsonify(milcoms_raw)
        return response
    flask.abort(404)

@app.route("/get/districts/<int:district_id>/milcoms/<int:milcom_id>")
def get_milcom(district_id:int, milcom_id:int):
    """
    Отримує координати військкомату за його номером та номером області

    Args:
        district_id (int): номер області (1..24)
        milcom_id (int): номер військкомату (1..n)
    Returns:
        flask.Response : HTTP відповідь з JSON даними та координатами обраного військкомату 
    """
    milcom_raw = sprotyv_parser.milcom_raw(district_id, milcom_id)
    milcom = MilCom(*milcom_raw).__dict__
    if milcom:
        response = flask.jsonify(milcom)
        return response
    flask.abort(404)

@app.route("/get/districts")
def get_districts():
    """
    Отримує всі координати військкоматів України + контактні дані де можливо

    Returns:
        flask.Response : HTTP відповідь з JSON даними та координатами всіх військкомати України
    """
    return generate_districts(), {
        "Content-Type": "application/json", 
        "Access-Control-Allow-Origin":'*' 
        }

@app.route("/get/districts/<int:district_id>")
def get_district(district_id:int):
    """
    Отримує всі координати військкоматів в області під номером district_id

    Args:
        district_id (int): номер області (1..24)
    Returns:
        flask.Response : HTTP відповідь з JSON даними про військкомати в окремій області
    """
    name, milcoms_raw = sprotyv_parser.district_raw(district_id)
    data = generate_milcoms(milcoms_raw)
    if data != [] and data != None:
        result = "{"
        result += f'"{name}":'
        result += json.dumps(data)
        result += '}'
        return result, {"Content-Type": "application/json"}
    flask.abort(404)

def generate_districts():
        """
        Генерує дані про військкомати у форматі:
        { "district":[...], "other":[...] }
        
        Returns: 
            Generator[str, None, None] : Генератор потокових даних про всі військкомати України
        """
        yield '{'
        # Отримання "сирих" військкоматів
        districts = list(sprotyv_parser.districts_raw().items())

        for i in range(len(districts)):
            # Розпаковка області
            name, milcoms_raw = districts[i]

            yield f'"{name}":'
            milcoms = generate_milcoms(milcoms_raw)
            yield json.dumps(milcoms)
            if i < len(districts)-1:
                yield ","
        yield '}'

def generate_milcoms(milcoms_raw:List[MilComRaw]) -> List[dict]:
    """
    Обробляє спарсені військкомати та фільтрує від пустих словників

    Args:
        milcoms_raw (List[MilComRaw]) : "сира" інформація про військкомати для обробки
    Returns:
        List[dict] : Представлення об'єктів MilCom у вигляді словників
    """
    return [milcom for milcom_raw in milcoms_raw if not is_empty(milcom := MilCom(*milcom_raw).__dict__)]

def is_empty(x):
    return x is None or x == {} or x == []
