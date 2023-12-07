"""This file contains all of the primitives needed by our flow."""

from buildflow.io.aws import S3Bucket
from buildflow.io.gcp import GCSBucket

from llama2_chat_bot.settings import env

# This primitive defines our bucket that contains our model.
if env.use_gcp:
    # If using GCP we use the GCSBucket primitive.
    model_bucket = GCSBucket(
        bucket_name=env.model_bucket, project_id=env.gcp_project_id
    )
else:
    # If using AWS we use the S3Bucket primitive.
    model_bucket = S3Bucket(bucket_name=env.model_bucket, aws_region=env.aws_region)
