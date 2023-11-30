import datetime

from buildflow import consumer
from buildflow.types.local import FileChangeEvent
from image_classification.dependencies import ModelDep
from image_classification.primitives import table, file_stream
from image_classification.schemas import Classification, ImageClassificationRow


@consumer(source=file_stream, sink=table)
def classify_image(
    file_event: FileChangeEvent, model: ModelDep
) -> ImageClassificationRow:
    predictions, probabilities = model.prediction.classifyImage(
        file_event.file_path, result_count=5
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
