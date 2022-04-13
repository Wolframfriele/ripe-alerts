from ninja import Schema
from pydantic import Field

from database.models import MeasurementType


class DetectionMethodOut(Schema):
    id: int
    type: str
    description: str


class AnomalyOut(Schema):
    id: int
    timestamp: str
    ip_address: str
    # autonomous_system: AutonomousSystem
    description: str
    measurement_type: MeasurementType
    detection_method: DetectionMethodOut
    medium_value: float
    value: float
    anomaly_score: float
    prediction_value: bool
    asn_error: int

    @staticmethod
    def resolve_timestamp(obj):
        return str(obj.time.year) + "-" + str(obj.time.month) + "-" + str(obj.time.day) + \
               " " + str(obj.time.hour) + ":" + str(obj.time.minute) + ":" + str(obj.time.second)


class AutonomousSystemSetting(Schema):
    monitor_possible: bool = Field(True, alias="Whether it is possible or not to monitor the given autonomous system.")
    host: str = Field("VODANET - Vodafone GmbH", alias="Hostname of the autonomous system.")
    message: str = Field("Success!", alias="Response from the server.")


class ASNumber(Schema):
    value: int = Field(1103, alias="as_number", description="The Autonomous system number to be set for the user for "
                                                            "monitoring. ")
