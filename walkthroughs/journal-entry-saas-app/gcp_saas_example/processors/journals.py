"""Define all of our endpoints four our CRUD API.

Each of these endpoints takes in the `RequiredStorageUserDep` this dependency
ensures the user is authenticated and registered in our database.

If either of these are false an exception will be raised. This means we can focus
on writing logic here and not worry about authentication or database setup.

Most of these endpoints also take in the `DB` dependency and user `with db.session as session`
This dependency uses a shared DB connection per replica and creates a new session per request.
"""

from buildflow import endpoint
from buildflow.exceptions import HTTPException

from gcp_saas_example import schemas
from gcp_saas_example.dependencies import RequiredStorageUserDep, DB
from gcp_saas_example.storage import models


def storage_journal_to_api(storage_journal: models.Journal) -> schemas.Journal:
    return schemas.Journal(
        id=str(storage_journal.id),
        title=storage_journal.title,
        content=storage_journal.entry,
        created_at=storage_journal.created_at,
    )


@endpoint("/journals/list", method="GET")
def list_journals(
    storage_user_db: RequiredStorageUserDep,
) -> schemas.ListJournalsResponse:
    storage_journals = storage_user_db.user.journals
    storage_journals.sort(key=lambda x: x.created_at, reverse=True)
    api_journals = []
    for storage_journal in storage_journals:
        api_journals.append(storage_journal_to_api(storage_journal))
    return schemas.ListJournalsResponse(api_journals)


@endpoint("/journals/create", method="POST")
def create_journal(
    journal: schemas.CreateJournalRequest,
    db: DB,
    storage_user_dep: RequiredStorageUserDep,
) -> schemas.Journal:
    with db.session as session:
        storage_journal = models.Journal(
            user_id=storage_user_dep.user.id, title=journal.title, entry=journal.content
        )
        session.add(storage_journal)
        session.commit()
        session.refresh(storage_journal)
        api_journal = storage_journal_to_api(storage_journal)
        return api_journal


@endpoint("/journals/update", method="POST")
def update_journal(
    journal: schemas.UpdateJournalRequest,
    db: DB,
    storage_user_dep: RequiredStorageUserDep,
) -> schemas.Journal:
    with db.session as session:
        storage_journal = session.query(models.Journal).get(journal.id)
        if storage_journal is None:
            raise HTTPException(404, "Journal not found")
        storage_journal.title = journal.title
        storage_journal.entry = journal.content
        session.commit()
        return storage_journal_to_api(storage_journal)


@endpoint("/journals/delete", method="POST")
def delete_journal(
    request: schemas.DeleteJournalRequest,
    db: DB,
    storage_user_dep: RequiredStorageUserDep,
):
    with db.session as session:
        storage_journal = session.query(models.Journal).get(request.id)
        if storage_journal is None:
            raise HTTPException(404, "Journal not found")
        session.delete(storage_journal)
        session.commit()
