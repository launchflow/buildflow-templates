"""Generated by BuildFlow."""
from buildflow import Flow

from data_warehouse_sync.processors.service import service


app = Flow()
app.add_service(service)
