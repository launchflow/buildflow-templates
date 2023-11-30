"""Define our endpoints for our model serving API.

We have two endpoints that are served by our service:
- index - Serves the index.html file.
- chat - Calls our model to generate a response to a chat message.
"""
from collections import deque

from buildflow import Service
from buildflow.responses import StreamingResponse, FileResponse

from launchflow_model_serving.dependencies import ModelDep
from launchflow_model_serving.schemas import ChatRequest
from launchflow_model_serving.settings import env

# Create our service.
# This service has 2 CPUs. This means that each replica will require 2 CPUs.
# All endpoints that are attached to the service will share the same 2 CPUs.
# We also scope our replicas to only 2 ongoing requests at a time. This is mainly
# because llama.cpp doesn't support any batching.
service = Service(
    service_id="model-service",
    num_cpus=env.cpus_pre_replics,
    max_concurrent_queries=2,
)


# Attach the `index` endpoint to our service.
@service.endpoint(route="/", method="GET")
def index() -> FileResponse:
    return FileResponse("launchflow_model_serving/processors/index.html")


# Attach the `index` endpoint to our service.
@service.endpoint(route="/chat", method="POST")
async def chat(
    request: ChatRequest,
    model_dep: ModelDep,
) -> StreamingResponse:
    llama_chat_messages = deque()
    request.messages.reverse()
    context_length = 0
    for message in request.messages:
        if context_length + len(message.message_content) > env.max_context_size:
            break
        llama_chat_messages.appendleft(
            {
                "role": message.chat_user.value,
                "content": message.message_content,
            }
        )

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
