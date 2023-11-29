"""Sample for how to schedule async tasks."""
import os
from typing import Dict

from buildflow import Flow
from buildflow.dependencies.sink import SinkDependencyBuilder
from buildflow.io.aws import SQSQueue
from buildflow.io.gcp import GCPPubSubTopic, GCPPubSubSubscription


app = Flow()
service = app.service(service_id="schedule-async-tasks")

gcp_pubsub_topic = GCPPubSubTopic(
    project_id=os.environ["GCP_PROJECT_ID"], topic_name="sample-topic"
)
gcp_pubsub_subscription = GCPPubSubSubscription(
    project_id=os.environ["GCP_PROJECT_ID"],
    subscription_name="sample-subscription",
).options(topic=gcp_pubsub_topic)

# sqs_queue = SQSQueue(queue_name="sample-queue")

app.manage(gcp_pubsub_topic, gcp_pubsub_subscription)
# app.manage(sqs_queue)


Sink = SinkDependencyBuilder(gcp_pubsub_topic)
# Sink = SinkDependencyBuilder(sqs_queue)


@service.endpoint("/square", method="GET")
async def square_endpoint(num: int, sink: Sink):
    await sink.push({"num": num})
    return {"success": True}


# @app.consumer(source=sqs_queue)
@app.consumer(source=gcp_pubsub_subscription)
def square_consumer(element: Dict[str, int]):
    square = element["num"] * element["num"]
    print(f"square of: {element['num']} is {square}")
