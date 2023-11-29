"""Define our collector processor.

For more information on collectors see: https://docs.buildflow.dev/programming-guide/collectors
"""

from buildflow import collector

from launchflow_collector_template.primitives import sink
from launchflow_collector_template.schemas import InputSchema, OutputSchema


@collector(sink=sink, route="/", method="POST")
def my_collector(input_data: InputSchema) -> OutputSchema:
    return OutputSchema(float_field=float(input_data.int_field) / 2)
