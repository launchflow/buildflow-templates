from buildflow import endpoint
from buildflow.exceptions import HTTPException
from buildflow.responses import RedirectResponse, FileResponse

from launchflow_chat.dependencies import StorageUserDep, DB
from launchflow_chat.schemas import ListSessionsResponse, GetSessionResponse
from launchflow_chat.storage.models import ChatSession, ChatMessageUser


@endpoint(route="/", method="GET")
def index(db: DB, storage_user: StorageUserDep):
    if storage_user.user is None:
        return RedirectResponse("/auth/login")
    return FileResponse("launchflow_chat/processors/index.html")


@endpoint(route="/list_sessions", method="GET")
def list_sessions(storage_user: StorageUserDep):
    if storage_user.user is None:
        return RedirectResponse("/auth/login")
    sessions = storage_user.user.chat_sessions
    responses = []
    for session in sessions:
        if len(session.chat_messages) == 0:
            continue
        responses.append(
            ListSessionsResponse(
                session_id=str(session.id),
                session_preview=session.chat_messages[0].message_content.removeprefix(
                    "User: "
                )[0:50],
            )
        )
    return responses


@endpoint(route="/get_session/{session_id}", method="GET")
def get_session(
    session_id: str, db: DB, storage_user: StorageUserDep
) -> GetSessionResponse:
    if storage_user.user is None:
        return RedirectResponse("/auth/login")
    session = db.session.query(ChatSession).get(session_id)
    if session is None:
        raise HTTPException(404, "Chat session not found")
    chat_messages = []
    for message in session.chat_messages:
        if message.chat_user == ChatMessageUser.USER:
            chat_messages.append(f"User: {message.message_content}")
        else:
            chat_messages.append(f"Assistant: {message.message_content}")
    chat = "\n\n".join([m for m in chat_messages])
    return GetSessionResponse(chat=chat)


@endpoint(route="/create_session", method="post")
def create_session(db: DB, storage_user: StorageUserDep) -> str:
    if storage_user.user is None:
        return RedirectResponse("/auth/login")
    session = db.session
    chat_session = ChatSession(user_id=storage_user.user.id)
    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)
    return str(chat_session.id)
