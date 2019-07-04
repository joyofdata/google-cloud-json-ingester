# google-cloud-json-ingester

## Deployment

```
./deploy.sh [project-id] [name of bucket for raw json data]
```

## Requests

```
curl -X POST -F "file=@[file name]" https://[project-id].appspot.com/upload
```
