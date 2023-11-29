"""Define any dependencies that our model serving API needs to run.

We have two dependencies here:
- ModelBucketDeb - Dependency with a reference to our bucket that contains the model.
- ModelDep - Dependency that loads the model from the bucket.

The ModelDep dependency is scoped to a Replica. This means that all requests send
to a single replica will share the same model. This is useful for caching the model
in memory and not having to reload it for every request.
"""

from asyncio import Lock
import logging
import os

from buildflow.dependencies import dependency, Scope
from buildflow.dependencies.bucket import BucketDependencyBuilder
from llama_cpp import Llama

from launchflow_model_serving.primitives import model_bucket
from launchflow_model_serving.settings import env

# This dependency loads a connection to the bucket containing our model.
ModelBucketDep = BucketDependencyBuilder(model_bucket)


@dependency(scope=Scope.REPLICA)
class ModelDep:
    """Dependency that downloads the model from the bucket, and sets up the model.

    NOTE: We use a lock around the model to ensure it is only accessed once per replica.
    This is because llama.cpp does not support batching at the moment. This lock is
    actually shared across all requests that are sent to a single replica. This means
    only one request per replica can access the model at a time.

    An alternative would be to use something like vllm: https://vllm.ai but we wanted
    to keep this example simple and easy to user for everyone.

    You can update the __init__ method to load in any custom model
    contained in your bucket.
    """

    def __init__(self, bucket_dep: ModelBucketDep):
        full_path = os.path.abspath(env.model_path)
        if not os.path.exists(full_path):
            logging.warning("Downloading model from bucket to: %s...", full_path)
            if env.use_gcp:
                # If using GCP we download the model using the cloud storage API.
                # https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob
                blob = bucket_dep.bucket.blob(env.model_path)
                blob.download_to_filename(full_path)
            else:
                # If using AWS we download the file using the boto3 library.
                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/download_file.html
                bucket_dep.bucket.download_file(env.model_path, full_path)
            logging.warning("... Finished downloading model from bucket.")
        self._llama_model = Llama(
            full_path,
            n_ctx=env.max_context_size,
            verbose=False,
            # NOTE: we set this equal to the number of replicas to ensure that each
            # replica stays self contained.
            n_threads=env.cpus_pre_replics,
        )
        self._lock = Lock()

    async def model(self):
        await self._lock.acquire()
        return self._llama_model

    def release(self):
        self._lock.release()
