# google-cloud-json-ingester

## Deployment

```
./deploy.sh [project-id] [name of bucket for raw json data] [Bigtable instance name] [BigQuery dataset name] [BigQuery table name]
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
