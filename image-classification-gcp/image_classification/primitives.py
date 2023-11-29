from buildflow.io.gcp import (
    GCSFileChangeStream,
    BigQueryTable,
    GCSBucket,
    BigQueryDataset,
)

from image_classification.settings import env
from image_classification.schemas import ImageClassificationRow

bucket = GCSBucket(
    project_id=env.gcp_project_id,
    bucket_name=f"{env.gcp_project_id}-image-classification",
).options(force_destroy=True)
file_change_stream = GCSFileChangeStream(gcs_bucket=bucket)

dataset = BigQueryDataset(
    project_id=env.gcp_project_id,
    dataset_name="buildflow_image_classification_walkthrough",
)
table = BigQueryTable(dataset=dataset, table_name="image_classification").options(
    schema=ImageClassificationRow
)
