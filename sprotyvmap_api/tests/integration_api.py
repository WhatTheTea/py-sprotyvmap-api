from flask import Flask
from sprotyvmap_api import endpoints as ep
from sprotyvmap_api.data.Point import Point
import pytest
import mock
import sprotyvmap_api
@pytest.fixture()
def app():
    app = sprotyvmap_api.flask_app
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    return app.test_cli_runner()


def test_raw_points_endpoint(client):
    response = client.get('/get/districts/raw')
    assert response.status_code == 200 and response.text

def test_point_endpoint_without_key(client):
    response = client.get('/get/districts/1/points/1')
    assert response.status_code == 401
    