from google.cloud import bigquery
from google.cloud import storage

import json
import datetime
import pytz
import os

import numpy as np


BIGQUERY_DATASET_NAME = os.environ.get("BIGQUERY_DATASET_NAME")
BIGQUERY_TABLE_NAME = os.environ.get("BIGQUERY_TABLE_NAME")
BUCKET_NAME_FOR_RAW_DATA = os.environ.get("BUCKET_NAME_FOR_RAW_DATA")


def store_data_in_bigquery(file, context):
    bq_dataset_name = BIGQUERY_DATASET_NAME
    bq_table_name = BIGQUERY_TABLE_NAME

    file_content = download_file_from_bucket(BUCKET_NAME_FOR_RAW_DATA, file["name"])
    data_dict = transform_data(file_content)

    client = bigquery.Client()
    dataset_ref = client.dataset(bq_dataset_name)
    table_ref = dataset_ref.table(bq_table_name)
    table = client.get_table(table_ref)

    rows = [
        {
            "dt": data_dict["ts"],
            "mean": data_dict["mn"],
            "std": data_dict["std"]
        }
    ]
    client.insert_rows(table, rows)

    return


def download_file_from_bucket(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)
    content = blob.download_as_string()
    return content


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
