import yaml
import os

import deploy_utils as du


config = yaml.load(open("deploy.yaml", "r"), Loader=yaml.FullLoader)

f_log = open("./deploy.log", "w+")

os.environ.setdefault(
    key="GOOGLE_APPLICATION_CREDENTIALS",
    value=config["project"]["google-application-credentials"]
)


du.replace_tokens_in_config_files(
    map_token_value=[
        ("PROJECT_ID", config["project"]["id"]),
        ("BUCKET_NAME_FOR_RAW_DATA", config["cloud-storage"]["raw-data-bucket"]["name"]),
        ("PUBSUB_NAME_CLOUD_STORAGE", config["pubsub"]["topics"][0]["name"])
    ],
    map_template_to_config=[
        (config["project"]["config-templates"]["app-yaml"],    config["project"]["config-files"]["app-yaml"]),
        (config["project"]["config-templates"]["openapi-yaml"],config["project"]["config-files"]["openapi-yaml"])
    ],
    f_log=f_log
)


bucket = config["cloud-storage"]["raw-data-bucket"]
du.create_storage_bucket(
    name=bucket["name"],
    location=bucket["location"],
    f_log=f_log
)

du.create_bigquery_datasets(
    datasets=config["bigquery"]["datasets"],
    f_log=f_log
)

du.create_bigquery_tables(
    project_id=config["project"]["id"],
    tables=config["bigquery"]["tables"],
    f_log=f_log
)

du.create_pubsub_topics(
    project_id=config["project"]["id"],
    topics=config["pubsub"]["topics"],
    f_log=f_log
)

du.deploy_cloud_functions(
    cloud_functions=config["cloud-functions"],
    cwd=os.getcwd(),
    f_log=f_log
)

du.deploy_endpoints_api(
    openapi_yaml=config["project"]["config-files"]["openapi-yaml"],
    cwd=os.getcwd(),
    f_log=f_log
)

du.deploy_appengine_app(
    app_yaml=config["project"]["config-files"]["app-yaml"],
    region=config["project"]["region"],
    cwd=os.getcwd(),
    f_log=f_log
)
