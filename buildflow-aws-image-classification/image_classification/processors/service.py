from buildflow import Service
from buildflow.requests import UploadFile
from buildflow.responses import FileResponse, HTMLResponse
import duckdb
import pandas as pd

from image_classification.dependencies import BucketDep
from image_classification.primitives import table

service = Service(service_id="image-classification")


@service.endpoint("/", method="GET")
def index():
    return FileResponse("image_classification/processors/index.html")


@service.endpoint("/image-upload", method="POST")
def image_upload(image_file: UploadFile, bucket_dep: BucketDep):
    bucket_dep.bucket.put_object(Key=image_file.filename, Body=image_file.file)


def generate_inner_table(row):
    inner_df = pd.DataFrame.from_records(row["classifications"])
    return inner_df.to_html(classes="table-auto", index=False, border=1).replace(
        "\n", ""
    )


@service.endpoint("/image-upload-results", method="GET")
def image_upload_results():
    conn = duckdb.connect(database=table.database, read_only=True)
    df = conn.execute(f"SELECT * FROM {table.table}").fetchdf()
    df["classifications"] = df.apply(generate_inner_table, axis=1)

    return HTMLResponse(
        df.to_html(
            classes="m-5 border-spacing-2 border-collapse border border-slate-500 table-auto".split(
                " "
            ),
            escape=False,
        ).replace("\n", "")
    )
