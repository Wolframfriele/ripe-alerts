from typing import Optional

from ninja import Schema
from pydantic import Field

from database.models import MeasurementType


class DetectionMethodOut(Schema):
    id: int = Field(1, alias="The id (primary key) of the detection method in the database. It can be used for "
                             "retrieving more information about the detection method. ")
    type: str = Field("ping", alias="Type of detection method.")
    description: str = Field("A1 Algorithm", alias="Short summary of the kind of detection method.")


class AnomalyOut(Schema):
    id: int = Field(1, alias="The id of the anomaly in the database.")
    timestamp: str = Field("2022-4-13 8:41:28", alias="Date and time when the anomaly occurred. Format: yyyy-mm-dd "
                                                      "hh:mm:ss")
    ip_address: str = Field("localhost", alias="Target address of Autonomous System")
    # autonomous_system: AutonomousSystem
    description: str = Field("Ping above 200ms for 5 minutes, normally 12ms.", alias="Explanation of the anomaly")
    measurement_type: MeasurementType
    detection_method: DetectionMethodOut
    medium_value: float = Field(40.122, alias="Average increase of round trip time (ms) at time of anomaly.")
    value: float = Field(12.144, alias="Average RTT (ms) at time of anomaly")
    anomaly_score: float = Field(22, alias="The strength of the anomaly? Percentage of probes that report an anomaly.")
    prediction_value: bool = Field(True,
                                   alias="User feedback, whether the prediction was accurate (True) or not. (False)")
    asn_error: int = Field(1402, alias="ASN of the router were the error happened.")

    @staticmethod
    def resolve_timestamp(obj):
        return str(obj.time.year) + "-" + str(obj.time.month) + "-" + str(obj.time.day) + \
               " " + str(obj.time.hour) + ":" + str(obj.time.minute) + ":" + str(obj.time.second)


class AutonomousSystemSetting(Schema):
    monitor_possible: bool = Field(True, alias="Whether it is possible or not to monitor the given autonomous system.")
    host: str = Field("VODANET - Vodafone GmbH", alias="Hostname of the autonomous system.")
    message: str = Field("Success!", alias="Response from the server.")


class AutonomousSystemSetting2(Schema):
    monitor_possible: bool = Field(True, alias="Whether it is possible or not to monitor the given autonomous system.")
    host: str = Field("VODANET - Vodafone GmbH", alias="Hostname of the autonomous system.")
    message: str = Field("Success!", alias="Response from the server.")
    autonomous_system: Optional[str] = Field("ASN1103", alias="The specified autonomous system")


class ASNumber(Schema):
    value: int = Field(1103, alias="as_number", description="The Autonomous system number to be set for the user for "
                                                            "monitoring. ")
