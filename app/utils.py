from google.cloud import storage

def store_object_in_bucket(bucket_name, object_name, object_data):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(object_data)
    return