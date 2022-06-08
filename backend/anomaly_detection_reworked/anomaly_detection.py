import threading
from typing import Type

from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_result_stream import MeasurementResultStream


class AnomalyDetection:

    def __init__(self):
        self.methods: dict[str, DetectionMethod] = {}
        self.thread = threading.Thread(target=MeasurementResultStream, args=([3534345, 9181644, 9181642],), daemon=True)

    def add_detection_method(self, method: DetectionMethod):
        """ Adds the detection method to the list.
            It is not possible to add new methods after calling start() method."""
        if not isinstance(method, DetectionMethod):
            raise TypeError("Input must be a valid DetectionMethod")
        self.methods[method.__class__.__name__] = method

    def remove_detection_method(self, method: Type[DetectionMethod]):
        self.methods.pop(method.__name__)

    def start(self):
        """ Starts the anomaly detection and connects to the Streaming API. """
        self.thread.start()
        for detection_method in self.methods.values():
            detection_method.on_startup_event()

    def stop(self):

        pass
        # self.thread.t

