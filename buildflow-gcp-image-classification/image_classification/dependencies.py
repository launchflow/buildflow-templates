import os

from buildflow.dependencies import dependency, Scope
from buildflow.dependencies.bucket import BucketDependencyBuilder
from imageai.Classification import ImageClassification

from image_classification.primitives import bucket


@dependency(scope=Scope.REPLICA)
class ModelDep:
    def __init__(self) -> None:
        self.execution_path = os.path.dirname(os.path.realpath(__file__))
        self.prediction = ImageClassification()
        self.prediction.setModelTypeAsMobileNetV2()
        self.prediction.setModelPath("mobilenet_v2-b0353104.pth")
        self.prediction.loadModel()


BucketDep = BucketDependencyBuilder(bucket)
