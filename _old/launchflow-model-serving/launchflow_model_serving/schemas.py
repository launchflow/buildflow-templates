"""Define all of the input and output schemas of our model serving API."""

import dataclasses
from enum import Enum
from typing import List


class ChatUser(Enum):
    """Who the chat message was from"""

    USER = "user"
    BOT = "assistant"


@dataclasses.dataclass
class ChatMessage:
    """An individual chat message."""

    message_content: str
    chat_user: ChatUser


@dataclasses.dataclass
class ChatRequest:
    """Expected requests from the client to /chat."""

    messages: List[ChatMessage]


@dataclasses.dataclass
class ChatResponse:
    """Response sent back to the client from /chat."""

    chunk: str
