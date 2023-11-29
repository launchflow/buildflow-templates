import dataclasses

from buildflow import Flow, FlowOptions
from buildflow.dependencies.sqlalchemy import engine

from launchflow_chat.processors.service import chat_service, base_service
from launchflow_chat.resources.database import cloud_sql_database, cloud_sql_instance
from launchflow_chat.settings import env
from launchflow_chat.storage import models


if env.create_models:
    models.Base.metadata.create_all(
        bind=engine(cloud_sql_database, env.database_user, env.database_password)
    )


@dataclasses.dataclass
class RequestSchema:
    prompt: str


app = Flow(
    flow_options=FlowOptions(
        gcp_service_account_info=env.gcp_service_account_info,
        stack=env.env.value,
    )
)
app.manage(cloud_sql_instance, cloud_sql_database)

app.add_service(chat_service)
app.add_service(base_service)
