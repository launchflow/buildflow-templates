"""Here we define the flow which is our main entry point of our project.

For more information see: https://docs.buildflow.dev/programming-guide/flows
"""
import os

from buildflow import Flow, FlowOptions

from launchflow_endpoint_template.settings import env


app = Flow(flow_options=FlowOptions(stack=env.env.value))

# Define a service object with a specific ID, all endpoints in this service
# will share the same resources (1 cpu since we didn't specify).
# https://docs.buildflow.dev/programming-guide/endpoints#service-options
service = app.service(service_id="hello-world-service")


# Add our hello world endpoint to the service.
@service.endpoint("/", method="GET")
def hello_world_endpoint() -> str:
    return f"Hello, from {os.getenv('HELLO_FROM', 'the void')}!"
