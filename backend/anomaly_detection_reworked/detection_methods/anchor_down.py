from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class AnchorDown(DetectionMethod):

    def on_result_response(self, data: dict):
        print("Anchor Down: " + str(data))

    def on_startup_event(self):
        print("Anchor Down loaded")
        pass

    @property
    def get_measurement_type(self) -> MeasurementType:
        return MeasurementType.ANCHORING
