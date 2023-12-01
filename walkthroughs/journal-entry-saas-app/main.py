"""Main file the setups the flow and is our entry point."""

from buildflow import Flow, FlowOptions
from buildflow.dependencies.sqlalchemy import engine
from journal_entry_saas.primitives import cloud_sql_database, cloud_sql_instance
from journal_entry_saas.processors.service import service
from journal_entry_saas.settings import env
from journal_entry_saas.storage import models

if env.create_models:
    models.Base.metadata.create_all(
        bind=engine(cloud_sql_database, env.database_user, env.database_password)
    )


app = Flow(flow_options=FlowOptions(stack=env.env.value))

app.manage(cloud_sql_instance, cloud_sql_database)
app.add_service(service)
