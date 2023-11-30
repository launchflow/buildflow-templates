"""Here we define the schemas that our consumer will use.

InputSchema - Defines the expected input of the consumer
OutputSchema - Defines the expected output of the consumer
"""

import dataclasses


@dataclasses.dataclass
class InputSchema:
    int_field: int


@dataclasses.dataclass
class OutputSchema:
    float_field: float
