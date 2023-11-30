"""Here we define the flow which is our main entry point of our project.

For more information see: https://docs.buildflow.dev/programming-guide/flows
"""
from buildflow import Flow, FlowOptions

from launchflow_consumer_template.processors.consumer import my_consumer
from launchflow_consumer_template.primitives import sink, source
from launchflow_consumer_template.settings import env


app = Flow(flow_options=FlowOptions(stack=env.env.value))

# Here we mark our primitives as managed so that `buildflow apply` will create / manage
# them
app.manage(sink, source)

app.add_consumer(my_consumer)
