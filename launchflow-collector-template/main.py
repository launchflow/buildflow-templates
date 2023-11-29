"""Here we define the flow which is our main entry point of our project.

For more information see: https://docs.buildflow.dev/programming-guide/flows
"""
from buildflow import Flow, FlowOptions

from launchflow_collector_template.processors.collector import my_collector
from launchflow_collector_template.primitives import sink
from launchflow_collector_template.settings import env


app = Flow(flow_options=FlowOptions(stack=env.env.value))

# Here we mark our primitives as managed so that `buildflow apply` will create / manage
# them
app.manage(sink)

app.add_collector(my_collector)
