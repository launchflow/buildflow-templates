from buildflow.io.gcp import GCSBucket

from launchflow_chat.settings import env

model_bucket = GCSBucket(
    project_id=env.model_bucket_project, bucket_name=env.model_bucket_name
)
