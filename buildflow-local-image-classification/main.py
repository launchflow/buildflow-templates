from buildflow import Flow

from image_classification.processors.consumer import classify_image
from image_classification.processors.service import service

app = Flow()
app.add_service(service)
app.add_consumer(classify_image)
