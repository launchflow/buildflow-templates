import dataclasses
import datetime
from typing import List


# Optional Step: Define a schema for the BigQuery table
@dataclasses.dataclass
class TableSchema:
    device_id: str
    timestamp: datetime.datetime
    average_value: float


# Define a schema for the HTTP requests
@dataclasses.dataclass
class RequestSchema:
    device_id: str
    timestamp: datetime.datetime
    values: List[float]
