import datetime
import os
import tempfile

from buildflow import consumer
from buildflow.types.aws import S3FileChangeEvent, S3ChangeStreamEventType

from image_classification.dependencies import ModelDep
from image_classification.primitives import table, source
from image_classification.schemas import Classification, ImageClassificationRow


@consumer(source=source, sink=table)
def classify_image(
    file_event: S3FileChangeEvent, model: ModelDep
) -> ImageClassificationRow:
    if file_event.event_type not in S3ChangeStreamEventType.create_event_types():
        # s3/sqs publishes a test notification when the notification is first created
        # we ignore that
        return
    with tempfile.TemporaryDirectory() as td:
        file_path = os.path.join(td, file_event.file_path)
        with open(file_path, "wb") as f:
            f.write(file_event.blob)
        predictions, probabilities = model.prediction.classifyImage(
            file_path, result_count=5
        )
    classifications = []
    for predicition, probability in zip(predictions, probabilities):
        classifications.append(Classification(predicition, probability))
    row = ImageClassificationRow(
        image_name=file_event.file_path,
        upload=datetime.datetime.utcnow().isoformat(),
        classifications=classifications,
    )
    print(row)
    return row
