import flask

app = flask.Flask(__name__)

@app.route("/")
def say_hi():
    return "<h1>hi</h1>"