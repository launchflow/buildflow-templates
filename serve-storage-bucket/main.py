"""Generated by BuildFlow."""
from buildflow import Flow

from serve_storage_bucket.processors.service import service


app = Flow()
app.add_service(service)