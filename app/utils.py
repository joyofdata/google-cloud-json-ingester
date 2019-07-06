import random
import string
import json
import numpy as np
import pytz
import datetime
import struct

from google.cloud import storage
from google.cloud import bigtable


def store_data_in_bigtable(
        data_dict,
        bt_instance_id,
        bt_table_name,
        bt_column_family_name_for_statistics
):
    client = bigtable.Client(admin=True)
    instance = client.instance(bt_instance_id)
    table = instance.table(bt_table_name)

    row_key = data_dict["ts"]
    row = table.row(row_key)
    row.set_cell(
        bt_column_family_name_for_statistics,
        "mean",
        struct.pack("d",data_dict["mn"]),
        timestamp=datetime.datetime.utcnow())
    row.set_cell(
        bt_column_family_name_for_statistics,
        "std",
        struct.pack("d",data_dict["std"]),
        timestamp=datetime.datetime.utcnow())
    row.commit()

    return


def store_object_in_bucket(
        bucket_name,
        object_name,
        object_data,
        prepend_random_string_to_object_name=False
):
    if prepend_random_string_to_object_name:
        length_of_prefix = 10
        rnd_string = ''.join(
            random.choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            ) for _ in range(length_of_prefix)
        )
        object_name = rnd_string + "-" + object_name

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(object_data)

    return


def transform_data(raw_data):
    data_0 = json.loads(raw_data)

    data_1 = {
        "ts": None,
        "mn": None,
        "std": None
    }

    data_1["ts"] = _convert_datetime_timezone_from_useastern_to_utc(data_0["time_stamp"])

    arr = np.asarray(data_0["data"])
    data_1["mn"] = arr.mean()
    data_1["std"] = arr.std()

    return data_1


def _convert_datetime_timezone_from_useastern_to_utc(dt):
    tz1 = pytz.timezone("US/Eastern")
    tz2 = pytz.timezone("UTC")

    dt = datetime.datetime.strptime(dt,"%Y-%m-%dT%H:%M:%S-04:00")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")

    return dt