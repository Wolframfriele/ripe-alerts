from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class RouteChange(DetectionMethod):
    """
    This Detection Method (algorithm) has not been finished. However, all methods work as supposed to.
    """

    def on_result_response(self, data: dict):
        pass

    def on_startup_event(self):
        pass

    @property
    def get_measurement_type(self) -> MeasurementType:
        return MeasurementType.TRACEROUTE

    @property
    def describe(self) -> tuple:
        return {
            "type": "Route Change",
            "Description": "Looks for route changes from neighboring connections that are not expected in comparison to baseline behaviour."
        }
