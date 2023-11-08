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

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    return app.test_cli_runner()

dummy_data_districts = [{'district':'1111', 'points':[Point('111','222','333').asdict(False)]},
                        {'district':'2222', 'points':[Point('333','222','333').asdict(False)]}]


@mock.patch("sprotyvmap_api.endpoints.dp", 
            point=lambda district_id, point_id : f"{district_id} {point_id}")
def test_mocking(mock_dp):
    assert ep.dp.point(1,1)  == '1 1'

    