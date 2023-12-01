"""This file contains all of the primitives needed by our flow."""


from buildflow.io.gcp import CloudSQLDatabase, CloudSQLInstance
from buildflow.types.gcp import CloudSQLDatabaseVersion, CloudSQLInstanceSettings

from journal_entry_saas.settings import env

# Deine our Cloud SQL instance in our GCP project.
cloud_sql_instance = CloudSQLInstance(
    instance_name="launchflow-gcp-postgres-auth-cloud-sql",
    project_id=env.gcp_project_id,
    database_version=CloudSQLDatabaseVersion.POSTGRES_15,
    region="us-central1",
    settings=CloudSQLInstanceSettings(
        tier=env.database_tier,
    ),
)

# Define our Cloud SQL database contained in our Cloud SQL instance.
cloud_sql_database = CloudSQLDatabase(
    instance=cloud_sql_instance,
    database_name="launchflow-gcp-postgres-auth-cloud-db",
)
