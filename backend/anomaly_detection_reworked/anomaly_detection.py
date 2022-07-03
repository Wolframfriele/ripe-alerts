from pydoc import describe
import threading
from typing import Type

from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_result_stream import MeasurementResultStream
from anomaly_detection_reworked.measurement_type import MeasurementType

# from database.models import DetectionMethod as DetectionMethodModel


class AnomalyDetection:

    def __init__(self):
        self.methods: dict[str, DetectionMethod] = {}

    def add_detection_method(self, method: DetectionMethod):
        """ Adds the detection method to the list.
            It is not possible to add new methods after calling start() method."""
        if not isinstance(method, DetectionMethod):
            raise TypeError("Input must be a valid DetectionMethod")
        elif not type(method.get_measurement_type) == MeasurementType:
            raise ValueError("Provide a valid MeasurementType in get_measurement_type()")
        self.methods[method.__class__.__name__] = method

    def remove_detection_method(self, method: Type[DetectionMethod]):
        self.methods.pop(method.__name__)

    def start(self):
        """ Starts the anomaly detection and connects to the Streaming API. """
        thread = threading.Thread(target=MeasurementResultStream,
                                  args=(self.methods.values(),), daemon=True)
        thread.start()
        for detection_method in self.methods.values():
            detection_method.on_startup_event()

    # def add_detection_methods_to_db(self) -> None:
    #     for method in self.methods:
    #         if not DetectionMethodModel.objects.exists(type=method.desribe["type"]):
    #             DetectionMethodModel.objects.create(
    #                 type=method.describe()["type"],
    #                 description=method.describe()["description"]
    #             )
