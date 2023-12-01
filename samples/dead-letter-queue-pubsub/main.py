import random
from dataclasses import dataclass

from buildflow import Flow
from buildflow.dependencies.sink import SinkDependencyBuilder
from buildflow.io.gcp import GCPPubSubSubscription, GCPPubSubTopic

# TODO(developer): Set this to your GCP project ID
GCP_PROJECT_ID = "your-gcp-project-id"

# The topic is where the messages are published.
dlq_topic = GCPPubSubTopic(
    project_id=GCP_PROJECT_ID,
    topic_name="dead-letter-queue-topic",
)
# The subscription is where the messages are received.
dlq_subscription = GCPPubSubSubscription(
    project_id=GCP_PROJECT_ID,
    subscription_name="dead-letter-queue-subscription",
).options(topic=dlq_topic, batch_size=1, enable_exactly_once_delivery=True)


app = Flow()

# Infrastructure state is managed by BuildFlow.
app.manage(dlq_topic, dlq_subscription)


@dataclass
class FailedPayload:
    message: str


@app.consumer(source=dlq_subscription)
def handle_errors(payload: FailedPayload):
    # TODO: Handle the error.
    print(f"Received error: {payload.message}")


# This is an example service that uses the dead letter queue.
service = app.service(service_id="service-id")

# This dependency builder lets us inject a sink that can be used to push data to
# the dead letter queue.
DLQ = SinkDependencyBuilder(dlq_topic)


@service.endpoint("/", "GET")
async def some_endpoint(dlq: DLQ):
    try:
        # Simulate an error.
        if random.random() < 0.5:
            raise Exception("Something went wrong!")
        return "Success!"
    except Exception as e:
        await dlq.push(FailedPayload(message=str(e)))
        return "Failure!"
