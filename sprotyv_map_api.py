import flask
import sprotyv_parser
import json
from typing import List
from sprotyv_milcom import MilCom, MilComRaw

app = flask.Flask(__name__)

@app.route("/get/districts/raw")
def get_raw_milcoms():
    """
    Отримує всі адреси воєнкоматів України + контактні дані
    """
    milcoms_raw = sprotyv_parser.districts_raw()
    if milcoms_raw:
        response = flask.jsonify(milcoms_raw)
        return response
    flask.abort(404)

@app.route("/get/districts/<int:district_id>/milcoms/<int:milcom_id>")
def get_milcom(district_id:int, milcom_id:int):
    """
    Отримує координати воєнкомату за його номером та номером області\n
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
    Отримує всі координати воєнкоматів України + контактні дані де можливо
    """
    return generate_districts(), {"Content-Type": "application/json"}

def generate_districts():
        """
        { "district":[...], "other":[...] }
        """
        yield '{'
        # Отримання "сирих" воєнкоматів
        districts = list(sprotyv_parser.districts_raw().items())

        for i in range(len(districts)):
            # Розпаковка області
            name, milcoms_raw = districts[i]

            yield f'"{name}":'
            milcoms = milcoms_generator()
            yield json.dumps(milcoms)
            if i < len(districts)-1:
                yield ","
        yield '}'

@app.route("/get/districts/<int:district_id>")
def get_district(district_id:int):
    """
    Отримує всі координати воєнкоматів в області під номером district_id
    """
    name, milcoms_raw = sprotyv_parser.district_raw(district_id)
    result = "{"
    result += f'"{name}":'
    result += json.dumps(milcoms_generator(milcoms_raw))
    result += '}'
    return result, {"Content-Type": "application/json"}

def milcoms_generator(milcoms_raw:List[MilComRaw]) -> List[dict]:
    """
    Обробляє спарсені воєнкомати та фільтрує від пустих словників
    """
    return [milcom for milcom_raw in milcoms_raw if not is_empty(milcom := MilCom(*milcom_raw).__dict__)]

def is_empty(x):
    return x is None or x == {} or x == []
