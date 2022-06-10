from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class AnchorDown(DetectionMethod):
    """
    This Detection Method (algorithm) has not been finished. However, all methods work as supposed to.
    """

    def on_result_response(self, data: dict):
        # LIST.
        # GET MSM ID -> ASN -> ANCHORS ->
        # GET ALL FQDN DOMAINS
        # PING ALL DOMAINS EVERY 30 SECONDS
        # IF NO RESPONSE -> CREATE AN ANOMALY
        #
        pass

    def on_startup_event(self):
        # print("Anchor Down loaded")
        pass

    @property
    def get_measurement_type(self) -> MeasurementType:
        return MeasurementType.PING
