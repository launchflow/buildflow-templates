"""Set up our service and "index" endpoint for serving our homepage."""

import uuid

from buildflow import Service
from buildflow.middleware import SessionMiddleware
from buildflow.responses import FileResponse, RedirectResponse

from journal_entry_saas.dependencies import MaybeStorageUserDep
from journal_entry_saas.processors import auth, journals

service = Service(service_id="journal-service")
# Add session middle ware to our service. This is required since we are storing
# authentication info in the session.
service.add_middleware(SessionMiddleware, secret_key=str(uuid.uuid4()))

# Attach all of our auth endpoints.
service.add_endpoint(auth.auth_login)
service.add_endpoint(auth.auth_callback)
service.add_endpoint(auth.auth_logout)

# Attach our CRUD endpoints.
service.add_endpoint(journals.create_journal)
service.add_endpoint(journals.list_journals)
service.add_endpoint(journals.update_journal)
service.add_endpoint(journals.delete_journal)


@service.endpoint("/", method="GET")
def index(storage_user_dep: MaybeStorageUserDep):
    if storage_user_dep.user is None:
        # If the user was not authed redirect to the login page.
        return RedirectResponse("/auth/login")
    return FileResponse("journal_entry_saas/processors/index.html")
