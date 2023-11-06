import flask
from sprotyvmap_api.endpoints import *
from sprotyvmap_api.data.Point import _geocoder as geocoder

flask_app = flask.Flask(__name__)

