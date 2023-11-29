"""Sample for how to manage resources with BuildFlow."""

import os

from buildflow import Flow
from buildflow.io.aws import S3Bucket
from buildflow.io.gcp import GCPPubSubTopic


app = Flow()

bucket = S3Bucket(bucket_name="my-bucket", aws_region="us-east-1")
topic = GCPPubSubTopic(topic_name="my-topic", project_id=os.environ["GCP_PROJECT_ID"])

app.manage(bucket, topic)
