from collections import deque

from buildflow import endpoint
from buildflow.exceptions import HTTPException
from buildflow.responses import StreamingResponse, RedirectResponse
from llama_cpp import ChatCompletionMessage

from launchflow_chat.dependencies import DB, ModelDep, StorageUserDep
from launchflow_chat.schemas import ChatRequest
from launchflow_chat.storage.models import ChatMessage, ChatMessageUser, ChatSession


@endpoint(route="/send_chat", method="POST")
def chat(
    request: ChatRequest,
    model_dep: ModelDep,
    storage_user: StorageUserDep,
    db: DB,
) -> StreamingResponse:
    if storage_user.user is None:
        return RedirectResponse("/auth/login")
    session = db.session
    chat_session = session.query(ChatSession).get(request.chat_session)
    if chat_session is None:
        raise HTTPException(404, "Chat session not found")
    session.add(
        ChatMessage(
            message_content=request.prompt,
            chat_user=ChatMessageUser.USER,
            chat_session_id=chat_session.id,
        )
    )

    messages = chat_session.chat_messages
    messages = (
        session.query(ChatMessage)
        .filter(ChatMessage.chat_session_id == chat_session.id)
        .order_by(ChatMessage.id.desc())
    )
    chat_completion_messages = deque()

    context_size = len(request.prompt)
    chat_completion_messages.append(
        ChatCompletionMessage(role="user", content=request.prompt)
    )

    for message in messages:
        context_size += len(message.message_content)
        if context_size > 512:
            break
        chat_completion_messages.appendleft(
            ChatCompletionMessage(
                role=message.chat_user.value, content=message.message_content
            )
        )
    chat_prediction = model_dep.llama_model.create_chat_completion(
        chat_completion_messages, stream=True
    )

    def iter_chunks():
        yield "Assistant: "
        message = ""
        for chunk in chat_prediction:
            if chunk.get("choices", []):
                choice = chunk["choices"][0]
                message_chunk = choice.get("delta", {}).get("content", "")
                message += message_chunk
                yield message_chunk
        session.add(
            ChatMessage(
                message_content=message,
                chat_user=ChatMessageUser.ASSISTANT,
                chat_session_id=chat_session.id,
            )
        )
        session.commit()
        session.close()

    session.commit()

    return StreamingResponse(iter_chunks())
