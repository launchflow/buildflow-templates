"""Here we define the flow which is our main entry point of our project.

For more information see: https://docs.launchflow.com/buildflow/programming-guide/flows
"""
from buildflow import Flow, FlowOptions
from buildflow_consumer.primitives import sink, source
from buildflow_consumer.processors.consumer import my_consumer
from buildflow_consumer.settings import env

app = Flow(flow_options=FlowOptions(stack=env.env.value))

# Here we mark our primitives as managed so that `buildflow apply` will create / manage
# them
app.manage(sink, source)

app.add_consumer(my_consumer)
