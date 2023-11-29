import os

from buildflow import Service
from buildflow.requests import UploadFile
from buildflow.responses import FileResponse, HTMLResponse
import duckdb
import pandas as pd

from image_classification.primitives import table

service = Service(service_id="image-classification")


@service.endpoint("/", method="GET")
def index():
    return FileResponse("image_classification/processors/index.html")


@service.endpoint("/image-upload", method="POST")
async def image_upload(image_file: UploadFile):
    new_file_path = os.path.join("image_folder", image_file.filename)
    with open(new_file_path, "wb") as f:
        file_bytes = await image_file.read()
        f.write(file_bytes)
    with open(new_file_path, "rb") as f:
        file_bytes = f.read()


def generate_inner_table(row):
    inner_df = pd.DataFrame.from_records(row["classifications"])
    return inner_df.to_html(
        classes="table-auto".split(" "),
        index=False,
        border=1,
    ).replace("\n", "")


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
