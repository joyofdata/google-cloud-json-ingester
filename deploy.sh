#!/usr/bin/env bash

# $1: google app engine project-id
# $2: name of bucket for raw json data
# $3: id of bigtable instance
# $4: name of bigquery dataset
# $5: name of bigquery table

announcement () {
    echo ""
    echo ">>>>> $1 ..."
    echo ""
}

announcement "set config values in YAML files"
sed "s/{{PROJECT_ID}}/$1/g" ./openapi_template.yaml > ./openapi.yaml
sed "
    s/{{PROJECT_ID}}/$1/g;
    s/{{BUCKET_NAME_FOR_RAW_DATA}}/$2/g;
    s/{{BIGTABLE_INSTANCE_ID}}/$3/g;
    s/{{BIGQUERY_DATASET_NAME}}/$4/g;
    s/{{BIGQUERY_TABLE_NAME}}/$5/g;
    " ./app/app_template.yaml > ./app/app.yaml

announcement "set region to Frankfurt if (still) possible"
gcloud app create --region="europe-west3"

announcement "create bucket for raw json data if it doesn't exist yet"
gsutil mb gs://$2/

# announcement "create table with column family"
# cbt createtable data -project $1 -instance $3
# cbt createfamily data statistics -project $1 -instance $3

announcement "deploy API"
gcloud endpoints services deploy "./openapi.yaml"

announcement "deploy app"
gcloud -q app deploy "./app/app.yaml"