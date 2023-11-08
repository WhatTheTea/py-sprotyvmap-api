import flask
import sprotyvmap_api.data.preprocessing as dp
from sprotyvmap_api.data.geocoder import GeocoderException

flask_app = flask.Flask(__name__)

@flask_app.route("/get/districts/raw")
def get_raw_points():
    """
    Отримує всі адреси військкоматів України + контактні дані

    Returns:
        flask.Response : HTTP відповідь з JSON даними про всі військкомати України
    """
    data = [ds for i in range(1,24+1) if (ds := dp.district(i))]
    for kv in data:
        kv["points"] = [p.asdict(False) for p in kv["points"]]
    if data:
        return flask.jsonify(data)
    flask.abort(flask.Response("Data was empty", 500))

@flask_app.route("/get/districts/<int:district_id>/points/<int:point_id>")
def get_point(district_id:int, point_id:int):
    """
    Отримує координати військкомату за його номером та номером області

    Args:
        district_id (int): номер області (1..24)
        point_id (int): номер військкомату (1..n)
    Returns:
        flask.Response : HTTP відповідь з JSON даними та координатами обраного військкомату 
    """
    try:
        data = dp.point(district_id, point_id).asdict()
        if data: return flask.jsonify(data)
    except GeocoderException as e:
        flask.abort(e.status)
    else:
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
