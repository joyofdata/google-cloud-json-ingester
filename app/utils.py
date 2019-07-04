import random
import string

from google.cloud import storage

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