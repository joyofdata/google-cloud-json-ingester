from google.cloud import storage

import random
import string
import json
import base64


def store_data_in_cloud_storage(data, context):
    args = json.loads(base64.b64decode(data["data"]).decode('utf-8'))

    bucket_name = args["bucket_name"]
    object_name = args["object_name"]
    object_data = args["object_data"]
    prepend_random_string_to_object_name = args["prepend_random_string_to_object_name"]

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