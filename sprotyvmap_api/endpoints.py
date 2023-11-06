import flask
import json
from typing import List
from sprotyvmap_api.data_preprocessing import Point

flask_app : flask.Flask

@flask_app.route("/get/districts/raw")
def get_raw_milcoms():
    """
    Отримує всі адреси військкоматів України + контактні дані

    Returns:
        flask.Response : HTTP відповідь з JSON даними про всі військкомати України
    """
    
    flask.abort(404)

@flask_app.route("/get/districts/<int:district_id>/milcoms/<int:milcom_id>")
def get_milcom(district_id:int, milcom_id:int):
    """
    Отримує координати військкомату за його номером та номером області

    Args:
        district_id (int): номер області (1..24)
        milcom_id (int): номер військкомату (1..n)
    Returns:
        flask.Response : HTTP відповідь з JSON даними та координатами обраного військкомату 
    """
    
    flask.abort(404)

@flask_app.route("/get/districts")
def get_districts():
    """
    Отримує всі координати військкоматів України + контактні дані де можливо

    Returns:
        flask.Response : HTTP відповідь з JSON даними та координатами всіх військкомати України
    """
    

@flask_app.route("/get/districts/<int:district_id>")
def get_district(district_id:int):
    """
    Отримує всі координати військкоматів в області під номером district_id

    Args:
        district_id (int): номер області (1..24)
    Returns:
        flask.Response : HTTP відповідь з JSON даними про військкомати в окремій області
    """
    
    flask.abort(404)
