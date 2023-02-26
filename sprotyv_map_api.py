import flask
import sprotyv_parser
import sprotyv_milcom

app = flask.Flask(__name__)

@app.route("/get/raw", methods=["GET"])
def get_raw_milcoms():
    milcoms_raw = [m._asdict() for m in sprotyv_parser.get_milcoms_raw()]
    response = flask.jsonify(milcoms_raw)
    return response

@app.route("/get/district/<int:district_id>/milcom/<int:milcom_id>")
def get_milcom(district_id:int, milcom_id:int):
    milcom_raw = sprotyv_parser.get_milcom_raw(district_id, milcom_id)
    milcom = sprotyv_milcom.get(*milcom_raw)
    if(milcom):
        milcom.location = milcom.location._asdict()
        response = flask.jsonify(milcom._asdict())
        return response
    response = flask.jsonify(f"Адресу {district_id}->{milcom_id} не було знайдено")
    response.status_code = 404
    return response
