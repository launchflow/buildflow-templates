import argparse
from pprint import pprint
import time
import sys

from google.cloud import bigquery
from google.cloud import storage


def upload(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to upload", default="founders_dog.jpg")
    parser.add_argument("--bucket", help="bucket to upload to", required=True)
    parser.add_argument(
        "--project", help="project to look for bq table in", required=True
    )
    parser.add_argument(
        "--table-name", help="name of table to query", default="image_classification"
    )
    parser.add_argument(
        "--dataset-name",
        help="name of dataset to query",
        default="buildflow_walkthrough",
    )
    parsed = parser.parse_args(args)

    storage_client = storage.Client()
    print("uploading image to bucket")
    storage_client.get_bucket(parsed.bucket).blob(parsed.image).upload_from_filename(
        parsed.image
    )
    print("waiting for 5 seconds for image to be processed")
    time.sleep(5)

    bigquery_client = bigquery.Client(parsed.project)
    query_job = bigquery_client.query(
        f"SELECT * FROM `{parsed.project}.{parsed.dataset_name}.{parsed.table_name}`"
    )
    rows = []
    for row in query_job:
        rows.append(dict(row.items()))

    print("results")
    print("-------")
    pprint(rows)


if __name__ == "__main__":
    upload(sys.argv[1:])
