from buildflow import Flow, FlowOptions

from image_classification import primitives
from image_classification.processors.consumer import classify_image
from image_classification.processors.service import service
from image_classification.settings import env

app = Flow(
    flow_options=FlowOptions(
        gcp_service_account_info=env.gcp_service_account_info, stack=env.env.value
    )
)
app.manage(
    primitives.bucket,
    primitives.dataset,
    primitives.table,
    primitives.file_change_stream,
)
app.add_service(service)
app.add_consumer(classify_image)
