from typing import Optional

from ninja import Schema
from pydantic import Field

from database.models import MeasurementType, Feedback


class AutonomousSystemSetting(Schema):
    monitor_possible: bool = Field(True,
                                   description="Whether it is possible or not to monitor the given autonomous system.")
    host: str = Field("VODANET - Vodafone GmbH", description="Hostname of the autonomous system.")
    message: str = Field("Success!", description="Response from the server.")


class AutonomousSystemSetting2(Schema):
    monitor_possible: bool = Field(True,
                                   description="Whether it is possible or not to monitor the given autonomous system.")
    host: str = Field("VODANET - Vodafone GmbH", description="Hostname of the autonomous system.")
    message: str = Field("Success!", description="Response from the server.")
    autonomous_system: Optional[str] = Field("ASN1103", description="The specified autonomous system")


class ASNumber(Schema):
    value: int = Field(1103, alias="as_number", description="The Autonomous system number to be set for the user for "
                                                            "monitoring. ")


class DetectionMethodOut(Schema):
    id: int = Field(1, description="The id (primary key) of the detection method in the database. It can be used for "
                                   "retrieving more information about the detection method. ")
    type: str = Field("ping", description="Type of detection method.")
    description: str = Field("A1 Algorithm", description="Short summary of the kind of detection method.")


class AnomalyOut(Schema):
    id: int = Field(1, description="The id of the anomaly in the database.")
    timestamp: str = Field("2022-4-13 8:41:28",
                           description="Date and time when the anomaly occurred. Format: yyyy-mm-dd "
                                       "hh:mm:ss")
    ip_address: list[str] = Field("localhost", description="Target address of Autonomous System")
    description: str = Field("Ping above 200ms for 5 minutes, normally 12ms.", description="Explanation of the anomaly")
    measurement_type: MeasurementType
    detection_method: DetectionMethodOut
    mean_increase: float = Field(40.122, description="Average increase of round trip time (ms) at time of anomaly.")
    anomaly_score: float = Field(22,
                                 description="The strength of the anomaly? Percentage of probes that report an anomaly.")
    prediction_value: bool = Field(True,
                                   description="Prediction by the Feedback Engine, "
                                               "whether the prediction was accurate (True) or not. (False)")
    asn: int = Field(1402, description="ASN of the router were the error happened.")
    feedback: Optional[bool] = Field(None, description="User feedback, whether the prediction was accurate (True) or "
                                                       "not. (False)")

    @staticmethod
    def resolve_timestamp(obj):
        return str(obj.time.year) + "-" + str(obj.time.month) + "-" + str(obj.time.day) + \
               " " + str(obj.time.hour) + ":" + str(obj.time.minute) + ":" + str(obj.time.second)

    @staticmethod
    def resolve_ip_address(obj):
        return str(obj.ip_address).replace(' ', '').split(",")

    @staticmethod
    def resolve_feedback(obj):
        return Feedback.get_feedback(obj.id)

