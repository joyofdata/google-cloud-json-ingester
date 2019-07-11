import yaml
import deploy_utils as du

config = yaml.load(open("deploy.yaml", "r"))

project_id = config["project-id"]


bucket = config["cloud-storage"]["raw-data-bucket"]
du.create_bucket(
    name=bucket["name"],
    location=bucket["location"]
)


datasets = config["bigquery"]["datasets"]
du.create_datasets(datasets=datasets)


tables = config["bigquery"]["tables"]
du.create_tables(project_id=project_id, tables=tables)