"""This file contains any primitive definitions that you may need in your flow.

For example if you needed a remote storagebucket:
- Google Cloud Storage: https://docs.buildflow.dev/primitives/gcp/gcs

    from buildflow.io.gcp import GCSBucket

    bucket = GCSBucket(project_id="project", bucket_name="bucket")

- Amazon S3: https://docs.buildflow.dev/primitives/aws/s3


    from buildflow.io.aws import S3Bucket

    bucket = S3Bucket(bucket_name="bucket", aws_region="us-east-1")

Then in main.py you can mark these as managed to have `buildflow apply` create / manage
them.

    app.manage(bucket)
"""

from buildflow.io.aws import SQSQueue

# TODO(developer): fill these in with a source. We use SQS as an example.
# A source can be any primitive that can be read from
# For example:
# - GCP Pub/Sub Subscription: https://docs.buildflow.dev/primitives/gcp/pubsub#gcp-pub-sub-subscription
# - GCS File Change Stream: https://docs.buildflow.dev/primitives/gcp/gcs_file_change_stream
# - AWS SQS: https://docs.buildflow.dev/primitives/aws/sqs
# - S3 File Change Stream: https://docs.buildflow.dev/primitives/gcp/gcs_file_change_stream
sink = SQSQueue(queue_name="input-queue")
# TODO(developer): fill these in with a sink. We use SQS as an example.
# A sink can be any primitive that can be written to
# For example:
# - GCP BigQuery Table: https://docs.buildflow.dev/primitives/gcp/bigquery#bigquerytable
# - GCP Pub/Sub Topic: https://docs.buildflow.dev/primitives/gcp/pubsub#gcp-pub-sub-topic
# - AWS SQS: https://docs.buildflow.dev/primitives/aws/sqs
# - DuckDB Table: https://docs.buildflow.dev/primitives/duckdb
source = SQSQueue(queue_name="input-queue")
