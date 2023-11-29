import dataclasses
from typing import List


@dataclasses.dataclass
class StringResponse:
    id: int
    string: str


@dataclasses.dataclass
class RetrieveResponse:
    strings: List[StringResponse]
