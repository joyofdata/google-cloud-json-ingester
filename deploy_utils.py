from google.cloud import storage
from google.cloud import bigquery


def create_tables(project_id, tables):
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

        table = bigquery.Table(full_table_id, schema=schema)
        client.create_table(table)


def create_datasets(datasets):
    client = bigquery.Client()

    for ds in datasets:
        if ds["id"] in [ds.dataset_id for ds in client.list_datasets()]:
            continue
        else:
            dataset_ref = client.dataset(ds["id"])
            dataset = bigquery.Dataset(dataset_ref)
            client.create_dataset(dataset)

    return


def create_bucket(name, location):
    client =  storage.Client()

    if name in [b.name for b in client.list_buckets()]:
        b = client.get_bucket(name)
        b.delete_blobs(blobs=b.list_blobs())
    else:
        b = storage.Bucket(client=client)
        b.name = name
        b.create(location=location)

    return
