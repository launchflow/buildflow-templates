"""Generated by BuildFlow."""
from buildflow import Flow

from llama_chat_bot.processors.service import service


app = Flow()
app.add_service(service)