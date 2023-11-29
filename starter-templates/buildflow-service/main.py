"""Here we define the flow which is our main entry point of our project.

For more information see: https://docs.launchflow.com/buildflow/programming-guide/flows
"""

from buildflow import Flow, FlowOptions
from buildflow_service.service import service
from buildflow_service.settings import env

# Your Flow is the container for your application.
app = Flow(flow_options=FlowOptions(stack=env.env.value))

app.add_service(service)