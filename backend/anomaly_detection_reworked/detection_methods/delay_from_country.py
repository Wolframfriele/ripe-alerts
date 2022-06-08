from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class DelayFromCountry(DetectionMethod):

    def on_result_response(self, data: dict):
        pass

    def on_startup_event(self):
        from database.models import MeasurementCollection  # CRUD functions are fully supported!
        measurement_collections_count = MeasurementCollection.objects.all().count()

    @property
    def get_measurement_type(self) -> MeasurementType:
        return MeasurementType.HTTP
