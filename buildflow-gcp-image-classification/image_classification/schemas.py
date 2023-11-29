import dataclasses
from typing import List


@dataclasses.dataclass
class Classification:
    classification: str
    confidence: float


@dataclasses.dataclass
class ImageClassificationRow:
    image_name: str
    upload: str
    classifications: List[Classification]
