from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class RouteChange(DetectionMethod):
    def on_result_response(self, data) -> None:
        pass

    def on_startup_event(self) -> None:
        pass

    @property
    def get_measurement_type(self) -> MeasurementType:
        pass