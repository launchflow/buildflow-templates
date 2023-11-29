"""Define all of the input and output schemas of our API."""

import dataclasses
import datetime
from typing import List


@dataclasses.dataclass
class DeleteJournalRequest:
    id: str


@dataclasses.dataclass
class UpdateJournalRequest:
    id: str
    title: str
    content: str


@dataclasses.dataclass
class CreateJournalRequest:
    title: str
    content: str


@dataclasses.dataclass
class Journal:
    id: str
    title: str
    content: str
    created_at: datetime.datetime


@dataclasses.dataclass
class ListJournalsResponse:
    journals: List[Journal]
