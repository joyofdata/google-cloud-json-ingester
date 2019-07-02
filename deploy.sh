#!/usr/bin/env bash

echo ""
echo ">>>>> replace project ID in YAML files ..."
echo ""
sed "s/{{PROJECT_ID}}/$1/g" ./openapi_template.yaml > ./openapi.yaml
sed "s/{{PROJECT_ID}}/$1/g" ./app/app_template.yaml > ./app/app.yaml

echo ""
echo ">>>>> deploy API ..."
echo ""
gcloud endpoints services deploy "./openapi.yaml"

# gcloud app create --region="europe-west3"

echo ""
echo ">>>>> deploy app ..."
echo ""
gcloud -q app deploy "./app/app.yaml"