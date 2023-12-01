import random
from dataclasses import dataclass

from buildflow import Flow
from buildflow.dependencies.sink import SinkDependencyBuilder
from buildflow.io.aws import SQSQueue

# TODO(developer): Set this to your AWS account ID
AWS_ACCOUNT_ID = "your-aws-account-id"

dead_letter_queue = SQSQueue(
    queue_name="dead-letter-queue",
    aws_account_id=AWS_ACCOUNT_ID,
    aws_region="us-west-2",
)

app = Flow()

# Infrastructure state is managed by BuildFlow.
app.manage(dead_letter_queue)


@dataclass
class FailedPayload:
    message: str


@app.consumer(source=dead_letter_queue)
def handle_errors(payload: FailedPayload):
    # TODO: Handle the error.
    print(f"Received error: {payload.message}")


# This is an example service that uses the dead letter queue.
service = app.service(service_id="service-id")

# This dependency builder lets us inject a sink that can be used to push data to
# the dead letter queue.
DLQ = SinkDependencyBuilder(dead_letter_queue)


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
