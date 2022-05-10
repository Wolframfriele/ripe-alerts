import datetime
from typing import List

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router, Path
from ninja.pagination import paginate, PageNumberPagination
from ninja.security import django_auth

from anomaly_detection.monitor_manager import MonitorManager
from database.models import AutonomousSystem, Setting, MeasurementCollection, Anomaly, MeasurementType, DetectionMethod
from ripe_interface.api_schemas import AutonomousSystemSetting, ASNumber, AutonomousSystemSetting2, AnomalyOut
from ripe_interface.requests import RipeRequests

router = Router()
"""Tags are used by Swagger to group endpoints."""
TAG = "RIPE Interface"


def get_username(request):
    default_user = 'admin'
    if hasattr(request, 'auth'):
        return str(request.auth)
    else:
        return default_user


@router.get("/generate-fake-anomalies", tags=[TAG])
def generate_fake_anomalies(request):
    """This endpoint is for testing purposes only! It adds fake anomalies to the database"""
    asn = ASNumber()
    asn.value = 1103
    response = set_autonomous_system_setting(request=None, asn=asn)
    if not response.status_code == 200:
        return JsonResponse({"message": "Something went wrong inside the server!"}, status=400)
    user = User.objects.get(username="admin")
    setting = Setting.objects.get(user=user)
    system = AutonomousSystem.objects.get(setting_id=setting.id)
    method = DetectionMethod.objects.create(type="ipv6 traceroute", description="a1 algorithm")
    method.save()
    Anomaly.objects.create(time=timezone.now(), ip_address="localhost, google.com", autonomous_system=system,
                           description="Ping above 100ms",
                           measurement_type=MeasurementType.TRACEROUTE, detection_method=method, mean_increase=2.1,
                           anomaly_score=4.0, prediction_value=False, asn=1402)
    return JsonResponse({"message": "Success!"}, status=200)


@router.get("/anomaly/{anomaly_id)", tags=[TAG])
def get_anomaly(request):  # TODO: edit router path
    """Retrieve an anomaly from the database."""
    Anomaly.objects.all()  # TODO: add filtering
    return "Hello worldooooo"


class DetectionMethodOut(Schema): #TODO: remove all schemes to schemes.py
    id: int
    type: str
    description: str


class AnomalyOut(Schema):
    id: int
    time: datetime.datetime
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


@router.get("/anomaly", response=List[AnomalyOut], tags=[TAG]) #TODO for later: add authentication
def list_anomalies(request):  # TODO: edit router path
    """Retrieve all anomalies from the database."""
    anomalies = Anomaly.objects.all()  # TODO: add filtering
    return anomalies


class AutonomousSystemSetting(Schema):
    monitor_possible: bool = Field(True, alias="Whether it is possible or not to monitor the given autonomous system.")
    host: str = Field("VODANET - Vodafone GmbH", alias="Hostname of the autonomous system.")
    message: str = Field("Success!", alias="Response from the server.")


class ASNumber(Schema):
    value: int = Field(1103, alias="as_number", description="The Autonomous system number to be set for the user for "
                                                            "monitoring. ")


@router.post("/{as_number}", response=AutonomousSystemSetting, tags=[TAG])
def set_autonomous_system_setting(request, asn: ASNumber = Path(...)):
    """To monitor a specific Autonomous System, we'll first need a valid Autonomous
    System Number (ASN). This endpoint validates and saves the ASN configuration in the database.  """
    asn_name = "ASN" + str(asn.value)
    if not RipeRequests.autonomous_system_exist(asn.value):
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": asn_name + " does not exist!"}, status=404)

    anchors = RipeRequests.get_anchors(asn.value)
    if len(anchors) == 0:
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": "There were no anchors found in " + asn_name},
                            status=404)

    asn_location = RipeRequests.get_company_name(asn.value)
    user_exists = User.objects.filter(username="admin").exists()
    if not user_exists:
        return JsonResponse({"monitoring_possible": False, "host": asn_location,
                             "message:": "User 'admin' does not exist!"}, status=400)

    user = User.objects.get(username="admin")
    user_configured = Setting.objects.filter(user=user).exists()
    if not user_configured:
        return JsonResponse({"monitoring_possible": False, "host": asn_location,
                             "message:": "User 'admin' settings is missing!"}, status=400)
    setting = Setting.objects.get(user=user)

    autonomous_system = AutonomousSystem.register_asn(setting=setting, system_number=asn.value, location=asn_location)
    MeasurementCollection.delete_all_by_asn(system=autonomous_system)
    monitor_manager = MonitorManager()
    for anchor in anchors:
        measurements = RipeRequests.get_anchoring_measurements(anchor.ip_v4)
        for measurement in measurements:
            monitor_mesh = measurement.save_to_database(system=autonomous_system)
            # monitor_manager.create_monitors(monitor_mesh)
            # break
    return JsonResponse({"monitoring_possible": True, "host": asn_location, "message": "Success!"}, status=200)
