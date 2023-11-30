from buildflow.io.gcp import CloudSQLInstance, CloudSQLDatabase
from buildflow.types.gcp import CloudSQLDatabaseVersion, CloudSQLInstanceSettings

from launchflow_chat.settings import env

cloud_sql_instance = CloudSQLInstance(
    instance_name="launchflow-chat-cloud-sql",
    project_id=env.gcp_project_id,
    database_version=CloudSQLDatabaseVersion.POSTGRES_15,
    region="us-central1",
    settings=CloudSQLInstanceSettings(
        tier=env.database_tier,
    ),
)
cloud_sql_database = CloudSQLDatabase(
    instance=cloud_sql_instance,
    database_name="launchflow-chat-db",
)
