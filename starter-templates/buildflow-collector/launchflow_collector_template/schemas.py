"""Here we define the schemas that our collector will use.

InputSchema - Defines the JSON payload of the collector endpoint
OutputSchema - Defines the expected output of the collector
"""

import dataclasses


@dataclasses.dataclass
class InputSchema:
    int_field: int


@dataclasses.dataclass
class OutputSchema:
    float_field: float
