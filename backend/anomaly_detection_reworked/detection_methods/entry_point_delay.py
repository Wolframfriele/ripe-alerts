from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class EntryPointDelay(DetectionMethod):
    @property
    def get_measurement_type(self) -> MeasurementType:
        pass

    def on_result_response(self, data):
        pass

    def on_startup_event(self):
        pass

