import uuid

from buildflow import Service
from buildflow.middleware import (
    SessionMiddleware,
)

from launchflow_chat.processors.chat import chat
from launchflow_chat.processors.auth import auth_login, auth_callback, auth_logout
from launchflow_chat.processors.index import (
    index,
    list_sessions,
    get_session,
    create_session,
)

session_secret = str(uuid.uuid4())

chat_service = Service(base_route="/chat", service_id="chat", num_cpus=2)
chat_service.add_endpoint(chat)
chat_service.add_middleware(SessionMiddleware, secret_key=session_secret)


base_service = Service(base_route="/", service_id="base", num_cpus=1)
base_service.add_middleware(SessionMiddleware, secret_key=session_secret)

base_service.add_endpoint(auth_login)
base_service.add_endpoint(index)
base_service.add_endpoint(auth_callback)
base_service.add_endpoint(auth_logout)
base_service.add_endpoint(list_sessions)
base_service.add_endpoint(get_session)
base_service.add_endpoint(create_session)
