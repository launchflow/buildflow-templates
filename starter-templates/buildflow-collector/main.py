"""Here we define the flow which is our main entry point of our project.

For more information see: https://docs.launchflow.com/buildflow/programming-guide/flows
"""
from buildflow import Flow, FlowOptions
from buildflow_collector.primitives import sink
from buildflow_collector.processors.collector import my_collector
from buildflow_collector.settings import env

app = Flow(flow_options=FlowOptions(stack=env.env.value))

# Here we mark our primitives as managed so that `buildflow apply` will create / manage
# them
app.manage(sink)

app.add_collector(my_collector)
