"""Define our collector processor.

For more information on collectors see: https://docs.launchflow.com/buildflow/programming-guide/collectors
"""

from buildflow import collector

from buildflow_collector.primitives import sink
from buildflow_collector.schemas import InputSchema, OutputSchema


@collector(sink=sink, route="/", method="POST")
def my_collector(input_data: InputSchema) -> OutputSchema:
    return OutputSchema(float_field=float(input_data.int_field) / 2)
