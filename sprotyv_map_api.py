import flask
import sprotyv_parser as parser

app = flask.Flask(__name__)

@app.route("/milcoms/raw/get")
def get_raw_milcoms():
    result = []
    milcoms = parser.get_milcoms()
    for m in milcoms:
        result.extend(m)
        result.append("\n")
    return "".join(result)
