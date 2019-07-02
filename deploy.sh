#!/usr/bin/env bash

sed "s/{{PROJECT_ID}}/$1/g" ./openapi_template.yaml > ./openapi.yaml
sed "s/{{PROJECT_ID}}/$1/g" ./app/app_template.yaml > ./app/app.yaml