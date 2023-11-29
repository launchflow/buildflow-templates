from buildflow.io.aws import S3FileChangeStream, S3Bucket
from buildflow.io.duckdb import DuckDBTable

from image_classification.settings import env

bucket = S3Bucket(
    bucket_name=env.s3_bucket_name,
    aws_region="us-east-1",
).options(force_destroy=True)

source = S3FileChangeStream(s3_bucket=bucket)
table = DuckDBTable(
    database="md:buildflow_walkthrough",
    table="image_classification",
    motherduck_token=env.motherduck_token,
)
