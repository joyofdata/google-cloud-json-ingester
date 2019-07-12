from google.cloud import storage
from google.cloud import bigquery
from google.cloud import pubsub_v1

import subprocess as sp


def replace_tokens_in_config_files(map_token_value, map_template_to_config, f_log):
    for (tf,cf) in map_template_to_config:
        with open(tf, "r") as h:
            tf_content = h.read()

        for (t,v) in map_token_value:
            tf_content = tf_content.replace("{{"+t+"}}", v)

        with open(cf, "w+") as h:
            h.write(tf_content)
    return


def deploy_appengine_app(app_yaml, region, cwd, f_log):
    log("---", f_log)
    log("deploy_appengine_app()", f_log)

    cmd = [
        "gcloud", "app", "create", "--region", region
    ]

    res = sp.Popen(cmd,
       stdout=f_log,
       stderr=f_log,
       cwd=cwd
       ).communicate()

    cmd = [
        "gcloud", "-q", "app", "deploy", app_yaml
    ]

    res = sp.Popen(cmd,
       stdout=f_log,
       stderr=f_log,
       cwd=cwd
       ).communicate()

    log("---", f_log)
    return


def deploy_endpoints_api(openapi_yaml, cwd, f_log):
    log("---", f_log)
    log("deploy_endpoints_api()", f_log)

    cmd = [
        "gcloud", "endpoints", "services", "deploy", openapi_yaml
    ]

    res = sp.Popen(cmd,
        stdout=f_log,
        stderr=f_log,
        cwd=cwd
    ).communicate()

    log("---", f_log)
    return


def deploy_cloud_functions(cloud_functions, cwd, f_log):
    log("---", f_log)
    log("deploy_cloud_functions()", f_log)

    for cf in cloud_functions:
        cmd = [
            "gcloud", "functions", "deploy",
            cf["name"],
            "--region", cf["region"],
            "--source", cf["source"],
            "--runtime", cf["runtime"]
        ]

        trigger = cf["trigger"]
        if trigger["type"] == "http":
            cmd += ["--trigger-http"]
        elif trigger["type"] == "topic":
            cmd += [
                "--trigger-topic", trigger["topic-name"]
            ]
        elif trigger["type"] == "bucket":
            cmd += [
                "--trigger-resource", trigger["bucket-name"],
                "--trigger-event", trigger["event-type"]
            ]
        else:
            raise Exception("unknown trigger type")

        if "env-vars" in cf:
            cmd += [
                "--set-env-vars",
                ",".join(
                    "{k}={v}".format(k=k, v=v)
                    for (k, v)
                    in cf["env-vars"].items()
            )]

        res = sp.Popen(cmd,
            stdout=f_log,
            stderr=f_log,
            cwd=cwd
        ).communicate()

    log("---", f_log)
    return


def create_pubsub_topics(project_id, topics, f_log):
    log("---", f_log)
    log("create_pubsub_topics()", f_log)

    client = pubsub_v1.PublisherClient()

    for t in topics:
        topic_path = client.topic_path(project=project_id, topic=t["name"])

        try:
            client.get_topic(topic=topic_path)
            log("PubSub tobic '{t}' already exists.".format(t=topic_path), f_log)
        except:
            client.create_topic(topic_path)
            log("PubSub tobic '{t}' created.".format(t=topic_path), f_log)

    log("---", f_log)
    return


def create_bigquery_tables(project_id, tables, f_log):
    log("---", f_log)
    log("create_bigquery_tables()", f_log)

    client = bigquery.Client()

    for t in tables:
        dataset_id = t["dataset-id"]
        full_table_id = "{p}.{d}.{t}".format(
            p=project_id,
            d=dataset_id,
            t=t["id"]
        )
        cols = t["columns"]

        schema = [
            bigquery.SchemaField(
                col["name"],
                col["type"],
                mode=col["mode"]
            ) for col in cols
        ]

        if t["id"] in [t.table_id for t in client.list_tables(dataset_id)]:
            log("BigQuery table '{t}' exists already.".format(t=t["id"]), f_log)
        else:
            table = bigquery.Table(full_table_id, schema=schema)
            client.create_table(table)
            log("BigQuery table '{t}' created.".format(t=t["id"]), f_log)


    log("---", f_log)
    return


def create_bigquery_datasets(datasets, f_log):
    log("---", f_log)
    log("create_bigquery_datasets()", f_log)

    client = bigquery.Client()

    for ds in datasets:
        if ds["id"] in [ds.dataset_id for ds in client.list_datasets()]:
            log("BigQuery dataset '{ds}' exists already.".format(ds=ds["id"]), f_log)
        else:
            dataset_ref = client.dataset(ds["id"])
            dataset = bigquery.Dataset(dataset_ref)
            client.create_dataset(dataset)
            log("BigQuery dataset '{ds}' created.".format(ds=ds["id"]), f_log)


    log("---", f_log)
    return


def create_storage_bucket(name, location, f_log):
    log("---", f_log)
    log("create_storage_bucket()", f_log)

    client =  storage.Client()

    if name in [b.name for b in client.list_buckets()]:
        b = client.get_bucket(name)
        b.delete_blobs(blobs=b.list_blobs())
        log("Storage bucket '{b}' exists already. Bucket was emptied.".format(b=name), f_log)
    else:
        b = storage.Bucket(client=client)
        b.name = name
        b.create(location=location)
        log("Storage bucket '{b}' created.".format(b=name), f_log)

    log("---", f_log)
    return


def log(text, f):
    f.write(text + "\n")
    f.flush()
