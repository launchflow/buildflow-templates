import datetime
import os
import tempfile

from buildflow import consumer
from buildflow.types.gcp import GCSFileChangeEvent

from image_classification.dependencies import ModelDep
from image_classification.primitives import table, file_change_stream
from image_classification.schemas import Classification, ImageClassificationRow


@consumer(source=file_change_stream, sink=table)
def classify_image(
    file_event: GCSFileChangeEvent, model: ModelDep
) -> ImageClassificationRow:
    with tempfile.TemporaryDirectory() as td:
        file_path = os.path.join(td, file_event.file_path)
        # Download the bytes to a local file that can be sent through the model
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
