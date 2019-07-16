import sys

sys.path.append(".")
import cloud_functions.store_data_in_bigquery.main as m


def test_transform_data():
    res =  m.transform_data(
        '{"time_stamp": "2019-05-02T06:00:00-04:00", "data": [1.2, 2.3, 3.4,4.5,5.6]}'
    )
    assert res["ts"] == '2019-05-02 10:00:00'
    assert abs(res["mn"] - 3.4) < 0.00001
    assert abs(res["std"] - 1.55563) < 0.00001



def test__convert_datetime_timezone_from_useastern_to_utc():
    assert m._convert_datetime_timezone_from_useastern_to_utc(
                "2019-04-03T13:34:53-04:00"
            ) == '2019-04-03 17:34:53'

    return