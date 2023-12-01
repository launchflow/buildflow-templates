import logging
import os

from buildflow.dependencies import Scope, dependency
from buildflow.dependencies.auth import AuthenticatedGoogleUserDepBuilder
from buildflow.dependencies.bucket import BucketDependencyBuilder
from buildflow.dependencies.sqlalchemy import SessionDepBuilder
from llama_cpp import Llama

from launchflow_chat.resources.database import cloud_sql_database
from launchflow_chat.resources.storage import model_bucket
from launchflow_chat.settings import env
from launchflow_chat.storage.models import User

ModelBucketDep = BucketDependencyBuilder(model_bucket)


@dependency(scope=Scope.REPLICA)
class ModelDep:
    def __init__(self, bucket_dep: ModelBucketDep):
        if not os.path.exists(env.model_path):
            logging.warning("Downloading model from bucket...")
            blob = bucket_dep.bucket.get_blob(env.model_path)
            self.model_bytes = blob.download_to_filename(env.model_path)
            logging.warning("... Finished downloading model from bucket.")
        self.llama_model = Llama(env.model_path, n_ctx=512)


DB = SessionDepBuilder(
    db_primitive=cloud_sql_database,
    db_user=env.database_user,
    db_password=env.database_password,
)


AuthenticatedGoogleUser = AuthenticatedGoogleUserDepBuilder(
    session_id_token="id_token", raise_on_unauthenticated=False
)


@dependency(scope=Scope.PROCESS)
class StorageUserDep:
    def __init__(self, db: DB, google_user: AuthenticatedGoogleUser) -> None:
        self.user = None
        if google_user.google_user is not None:
            self.user = (
                db.session.query(User)
                .filter(User.google_id == google_user.google_user.google_account_id)
                .first()
            )
            if self.user is None:
                self.user = User(google_id=google_user.google_user.google_account_id)
                db.session.add(self.user)
                db.session.commit()
