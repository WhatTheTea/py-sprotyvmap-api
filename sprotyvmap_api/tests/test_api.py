from sprotyvmap_api import endpoints as ep
import pytest
import mock

@mock.patch("sprotyvmap_api.endpoints.dp")
def test_returns_raw_data(dp):
    dp.point.side_effect = lambda district_id, point_id : f"{district_id} {point_id}"

    assert ep.dp.point(1,1) == '1 1'
    