"""Define any dependencies that our API needs to run.

We have serveral dependencies here:
- DB - sets up a database connection (per replica) and a sql alchemy session (pre request)
- MaybeAuthenticatedGoogleUser - sets up a google user if the user is authenticated
- RequiredAuthenticatedGoogleUser - sets up a google user if the user is authenticated, otherwise raises an exception
- MaybeStorageUser - fetchs or stores the user if the user is authenticated
- RequiredStorageUser - fetchs the user if the user is authenticated, otherwise raises an exception


"""

from buildflow.dependencies import dependency, Scope
from buildflow.dependencies.auth import AuthenticatedGoogleUserDepBuilder
from buildflow.dependencies.sqlalchemy import SessionDep
from buildflow.exceptions import HTTPException

from gcp_saas_example.settings import env
from gcp_saas_example.storage.models import User
from gcp_saas_example.primitives import cloud_sql_database

# This dependency sets up a database connection (per replica) and a sql alchemy session (pre request)
DB = SessionDep(
    db_primitive=cloud_sql_database,
    db_user=env.database_user,
    db_password=env.database_password,
)


# Set up a google user if the user is authenticated
# We use `session_id_token` to indicate we can use "token_id" from the session
# to fetch the user id token.
MaybeAuthenticatedGoogleUser = AuthenticatedGoogleUserDepBuilder(
    session_id_token="id_token", raise_on_unauthenticated=False
)
# Set up a google user if the user is authenticated, otherwise raises an exception
# We use `session_id_token` to indicate we can use "token_id" from the session
# to fetch the user id token.
RequiredAuthenticatedGoogleUser = AuthenticatedGoogleUserDepBuilder(
    session_id_token="id_token"
)


# Fetchs or stores the user if the user is authenticated
@dependency(scope=Scope.PROCESS)
class MaybeStorageUserDep:
    def __init__(self, db: DB, google_user: MaybeAuthenticatedGoogleUser) -> None:
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


# Fetchs the user if the user is authenticated, otherwise raises an exception
@dependency(scope=Scope.PROCESS)
class RequiredStorageUserDep:
    def __init__(self, db: DB, google_user: MaybeAuthenticatedGoogleUser) -> None:
        self.user = (
            db.session.query(User)
            .filter(User.google_id == google_user.google_user.google_account_id)
            .first()
        )
        if self.user is None:
            raise HTTPException(403, "user not found")
