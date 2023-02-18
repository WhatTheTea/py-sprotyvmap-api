import flask
import sprotyv_parser as parser

app = flask.Flask(__name__)

@app.route("/milcoms/get/raw", methods=["GET"])
def get_raw_milcoms():
    milcoms_raw = [m._asdict() for m in parser.get_milcoms_raw()]
    response = flask.jsonify(milcoms_raw)
    response.status_code = 200
    return response
