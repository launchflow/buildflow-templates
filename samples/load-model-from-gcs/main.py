"""Sample for how to load a model stored on a remote bucket."""
import logging
import os
from asyncio import Lock

from buildflow import Flow
from buildflow.dependencies import Scope, dependency
from buildflow.dependencies.bucket import BucketDependencyBuilder
from buildflow.io.gcp import GCSBucket
from buildflow.responses import StreamingResponse
from llama_cpp import Llama

# TODO(developer): Set this to your GCP project ID
GCP_PROJECT_ID = "your-gcp-project-id"

app = Flow()
service = app.service(service_id="model-loading")

bucket = GCSBucket(project_id=GCP_PROJECT_ID, bucket_name="launchflow-llama-models")
ModelBucketDep = BucketDependencyBuilder(bucket)


@dependency(scope=Scope.REPLICA)
class ModelDep:
    def __init__(self, bucket_dep: ModelBucketDep):
        full_path = os.path.abspath("llama-2-7b-chat.Q8_0.gguf")
        if not os.path.exists(full_path):
            logging.info("Downloading model from S3")
            bucket_dep.bucket.download_file("llama-2-7b-chat.Q8_0.gguf", full_path)
        self._llama_model = Llama(full_path, verbose=False)
        self._lock = Lock()

    async def model(self):
        await self._lock.acquire()
        return self._llama_model

    def release(self):
        self._lock.release()


@service.endpoint(route="/chat", method="POST")
async def chat(
    prompt: str,
    model_dep: ModelDep,
) -> StreamingResponse:
    llama_chat_messages = [{"role": "user", "content": prompt}]

    model = await model_dep.model()
    try:
        chat_prediction = model.create_chat_completion(llama_chat_messages, stream=True)
    except Exception as e:
        model_dep.release()
        raise e

    def iter_chunks():
        try:
            for chunk in chat_prediction:
                if chunk.get("choices", []):
                    choice = chunk["choices"][0]
                    message_chunk = choice.get("delta", {}).get("content", "")
                    yield message_chunk
        finally:
            model_dep.release()

    return StreamingResponse(iter_chunks())
