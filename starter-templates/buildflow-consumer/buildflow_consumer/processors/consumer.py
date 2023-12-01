"""Define our consumer processor.

For more information on consumers see: https://docs.buildflow.dev/programming-guide/consumers
"""

from buildflow import consumer
from buildflow_consumer.primitives import sink, source
from buildflow_consumer.schemas import InputSchema, OutputSchema


@consumer(source=source, sink=sink)
def my_consumer(input_data: InputSchema) -> OutputSchema:
    return OutputSchema(float_field=float(input_data.int_field) / 2)
