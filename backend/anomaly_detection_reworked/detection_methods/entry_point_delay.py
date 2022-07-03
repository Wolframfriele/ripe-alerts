from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class EntryPointDelay(DetectionMethod):
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
            "type": "Entry Point Delay",
            "description": "The entry delay detector finds the hop where packets enter into your own AS, \
            it then uses a sliding window to detect unexpected increases in round trip time."
        }
