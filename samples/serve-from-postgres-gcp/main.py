"""Sample for how to serve data from postgres."""
import os

import aiohttp.client_exceptions
from buildflow import Flow
from buildflow.dependencies.sqlalchemy import SessionDepBuilder, engine
from buildflow.io.gcp import CloudSQLDatabase, CloudSQLInstance, CloudSQLUser
from buildflow.types.gcp import CloudSQLDatabaseVersion, CloudSQLInstanceSettings
from serve_from_postgres import api_schemas, models

app = Flow()
service = app.service(service_id="serve-from-postgres")

cloud_sql_instance = CloudSQLInstance(
    instance_name="launchflow-serve-from-postgres",
    project_id=os.environ["GCP_PROJECT_ID"],
    database_version=CloudSQLDatabaseVersion.POSTGRES_15,
    region="us-central1",
    settings=CloudSQLInstanceSettings(tier="db-custom-1-3840"),
)

cloud_sql_database = CloudSQLDatabase(
    instance=cloud_sql_instance,
    database_name="launchflow-serve-from-postgres-db",
)

cloud_sql_user = CloudSQLUser(
    instance=cloud_sql_instance,
    user_name="my-user",
    password="my-password",
)

app.manage(cloud_sql_instance, cloud_sql_database, cloud_sql_user)

DB = SessionDepBuilder(
    db_primitive=cloud_sql_database,
    db_user=os.environ["DB_USER"],
    db_password=os.environ["DB_PASSWORD"],
)


try:
    models.Base.metadata.create_all(
        bind=engine(
            cloud_sql_database, os.environ["DB_USER"], os.environ["DB_PASSWORD"]
        )
    )
except aiohttp.ClientResponseError as e:
    if e.status != 404:
        raise e


@service.endpoint("/store", method="POST")
def store_string(string: str, db: DB):
    with db.session as session:
        session.add(models.Strings(string=string))
        session.commit()
    return {"status": "success"}


@service.endpoint("/retrieve", method="GET")
def retrieve_string(db: DB) -> api_schemas.RetrieveResponse:
    with db.session as session:
        strings = session.query(models.Strings).all()
        string_responses = []
        for string in strings:
            string_responses.append(
                api_schemas.StringResponse(id=string.id, string=string.string)
            )
        return api_schemas.RetrieveResponse(strings=string_responses)
