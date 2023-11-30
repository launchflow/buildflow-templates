import dataclasses
import json
from typing import Optional


@dataclasses.dataclass
class ChatRequest:
    prompt: str
    chat_session: Optional[str] = None


@dataclasses.dataclass
class ChatResponse:
    chunk: str
    chat_session: str

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))


@dataclasses.dataclass
class ListSessionsResponse:
    session_id: str
    session_preview: str


@dataclasses.dataclass
class GetSessionResponse:
    chat: str
