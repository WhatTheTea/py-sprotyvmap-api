import flask
import sprotyv_parser
import sprotyv_milcom

app = flask.Flask(__name__)

@app.route("/get/districts/raw", methods=["GET"])
def get_raw_milcoms():
    milcoms_raw = [m._asdict() for m in sprotyv_parser.milcoms_raw()]
    if milcoms_raw:
        response = flask.jsonify(milcoms_raw)
        return response
    flask.abort(404)

@app.route("/get/districts/<int:district_id>/milcoms/<int:milcom_id>")
def get_milcom(district_id:int, milcom_id:int):
    milcom_raw = sprotyv_parser.milcom_raw(district_id, milcom_id)
    milcom = sprotyv_milcom.get(*milcom_raw)
    if milcom:
        response = flask.jsonify(milcom._asdict())
        return response
    flask.abort(404)

@app.route("/get/districts")
def get_milcoms():
    milcoms_raw = [sprotyv_milcom.get(*milcom) for milcom in sprotyv_parser.milcoms_raw()]
    milcoms = [milcom._asdict() for milcom in milcoms_raw if milcom]
    if milcoms:
        response = flask.jsonify(milcoms)
        return response
    flask.abort(404)

