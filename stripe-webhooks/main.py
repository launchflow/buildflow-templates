"""Generated by BuildFlow."""
from buildflow import Flow

from stripe_webhooks.processors.service import service


app = Flow()
app.add_service(service)