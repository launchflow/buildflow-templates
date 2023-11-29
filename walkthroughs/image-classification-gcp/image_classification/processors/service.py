from buildflow import Service
from buildflow.requests import UploadFile
from buildflow.responses import FileResponse, HTMLResponse
from google.cloud import bigquery
import pandas as pd

from image_classification.dependencies import BucketDep
from image_classification.primitives import table

service = Service(service_id="image-classification")


@service.endpoint("/", method="GET")
def index():
    return FileResponse("image_classification/processors/index.html")


@service.endpoint("/image-upload", method="POST")
def image_upload(image_file: UploadFile, bucket_dep: BucketDep):
    blob = bucket_dep.bucket.blob(image_file.filename)
    blob.upload_from_file(image_file.file)


def generate_inner_table(row):
    inner_df = pd.DataFrame.from_records(row["classifications"])
    return inner_df.to_html(classes="table-auto", index=False, border=1).replace(
        "\n", ""
    )


@service.endpoint("/image-upload-results", method="GET")
def image_upload_results():
    bigquery_client = bigquery.Client()
    results = bigquery_client.query(f"SELECT * FROM {table.primitive_id()}")
    df = results.to_dataframe()
    df["classifications"] = df.apply(generate_inner_table, axis=1)

    return HTMLResponse(
        df.to_html(
            classes="m-5 border-spacing-2 border-collapse border border-slate-500 table-auto".split(
                " "
            ),
            escape=False,
        ).replace("\n", "")
    )
