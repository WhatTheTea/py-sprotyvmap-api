import flask
import sprotyv_parser
from sprotyv_milcom import MilCom, MilComRaw
from json import dumps as tojson

app = flask.Flask(__name__)

@app.route("/get/districts/raw", methods=["GET"])
def get_raw_milcoms():
    milcoms_raw = sprotyv_parser.districts_raw()
    if milcoms_raw:
        response = flask.jsonify(milcoms_raw)
        return response
    flask.abort(404)

@app.route("/get/districts/<int:district_id>/milcoms/<int:milcom_id>")
def get_milcom(district_id:int, milcom_id:int):
    milcom_raw = sprotyv_parser.milcom_raw(district_id, milcom_id)
    milcom = MilCom(*milcom_raw)
    if milcom:
        response = flask.jsonify(milcom)
        return response
    flask.abort(404)

@app.route("/get/districts")
def get_milcoms():
    """
    Отримує всі координати воєнкоматів України
    ! Виконання цього запиту займає багато часу, див. MilCom\n
    """
    def get():
        """
        { "district":[...], "other":[...] }
        """
        yield '{'
        districts = list(sprotyv_parser.districts_raw().items())
        for i in range(len(districts)):
            name, milcoms = districts[i]
            yield f'"{name}":'
            yield tojson([MilCom(*milcom).__dict__ for milcom in milcoms])
            if i < len(districts)-1:
                yield ","
        yield '}'
    return get(), {"Content-Type": "application/json"}

