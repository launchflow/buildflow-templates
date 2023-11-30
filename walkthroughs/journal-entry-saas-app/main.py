"""Main file the setups the flow and is our entry point."""

from buildflow import Flow, FlowOptions
from buildflow.dependencies.sqlalchemy import engine

from gcp_saas_example.processors.service import service
from gcp_saas_example.settings import env
from gcp_saas_example.storage import models
from gcp_saas_example.primitives import cloud_sql_database, cloud_sql_instance

if env.create_models:
    models.Base.metadata.create_all(
        bind=engine(cloud_sql_database, env.database_user, env.database_password)
    )


app = Flow(flow_options=FlowOptions(stack=env.env.value))

app.manage(cloud_sql_instance, cloud_sql_database)
app.add_service(service)
