# google-cloud-json-ingester

## Deployment

```
./deploy.sh \
    [project ID] \
    [name of bucket for raw JSON data] \
    [Bigtable instance name] \
    [BigQuery dataset name] \
    [BigQuery table name]
```

## Requests

```
curl -X POST -F "file=@[file name]" https://[project-id].appspot.com/upload?key=[API Key]
```

## Expected File Structure (Example)

```
{"time_stamp": "2019-05-02T06:00:00-04:00", "data": [1.2, 2.3, 3.4]}
```

## Infrastructure

App Engine app running as Flask web server exposes a Swagger 2.0 specified REST interface. Upon reception of a file
it pushes a message on a PubSub queue triggering the files storage on Cloud Storage by means of a Cloud Function.
Cloud Storage in turn triggers another Cloud Function transforming the data and storing it on BigQuery.

## Tests

Unit test may be performed by `pytest`.

```bash
➜  google-cloud-json-ingester git:(master) pytest
============================= test session starts ==============================
platform linux -- Python 3.6.8, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: /home/raffael/gitrepos/google-cloud-json-ingester
collected 3 items

cloud_functions/store_data_in_bigquery/tests/test_main_bigquery.py ..    [ 66%]
cloud_functions/store_data_in_cloud_storage/tests/test_main_storage.py . [100%]

=========================== 3 passed in 8.18 seconds ===========================
```