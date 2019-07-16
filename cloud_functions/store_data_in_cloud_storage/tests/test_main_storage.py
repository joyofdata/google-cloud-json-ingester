import yaml
import os
import sys
import random
import string
import json
import base64
import time

from google.cloud import storage

sys.path.append(".")
import cloud_functions.store_data_in_cloud_storage.main as m

config = yaml.safe_load(open("deploy.yaml", "r"))
os.environ.setdefault(
    key="GOOGLE_APPLICATION_CREDENTIALS",
    value=config["project"]["google-application-credentials"]
)


def test_store_data_in_cloud_storage():
    rnd_string = ''.join(
        random.choice(
            string.ascii_lowercase + string.digits
        ) for _ in range(20)
    )

    client =  storage.Client()

    b = storage.Bucket(client=client)
    b.name = "test-" + rnd_string
    b.create(location="europe-west3")

    data = {
        "bucket_name": b.name,
        "object_name": "test.json",
        "object_data": '{"time_stamp": "2019-05-02T06:00:00-04:00", "data": [1.2, 2.3, 3.4,4.5,5.6]}',
        "prepend_random_string_to_object_name": True
    }

    data_packed = {"data": base64.b64encode(json.dumps(data).encode('utf-8'))}

    m.store_data_in_cloud_storage(data_packed, None)

    time.sleep(1)

    try:
        b = client.get_bucket(b.name)
        blob_name = [blob.name for blob in b.list_blobs()][0]
        blob = b.get_blob(blob_name)
        content = blob.download_as_string()
    except:
        raise Exception("File 'test.json' not available from bucket '{}'.".format(b.name))

    assert content.decode("utf-8") == data["object_data"]

    b.delete_blobs(blobs=b.list_blobs())
    b.delete()

    return
