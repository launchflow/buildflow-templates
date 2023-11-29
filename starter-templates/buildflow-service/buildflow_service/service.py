"""Here we define the Service which exposes the endpoints for our application.

For more information see: https://docs.launchflow.com/buildflow/programming-guide/endpoints
"""

from buildflow import Service

from buildflow_service.settings import env

# Define a Service object with a specific ID, all endpoints in this service
# will share the same resources (1 cpu since we didn't specify).
# https://docs.launchflow.com/buildflow/programming-guide/endpoints#service-options
service = Service(service_id="buildflow-service")


# Add our hello world endpoint to the service.
@service.endpoint("/", method="GET")
def hello_world_endpoint() -> str:
    return f"Hello, from {env.env.value}!"
