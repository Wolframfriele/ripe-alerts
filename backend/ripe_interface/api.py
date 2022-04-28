from typing import List

from django.contrib.auth.models import User
from django.http import JsonResponse
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
        return JsonResponse({"message": response.get('message')}, status=response.status_code)
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


@router.get("/anomaly", response=List[AnomalyOut], tags=[TAG])  # TODO for later: add authentication
@paginate(PageNumberPagination)
def list_anomalies(request):
    """Retrieves all anomalies by user from the database.  """
    system = AutonomousSystem.get_asn_by_username(username="admin")
    anomalies = Anomaly.objects.filter(autonomous_system=system)
    if anomalies is None:
        return []
    return anomalies


@router.get("/", response=AutonomousSystemSetting2, tags=[TAG])
def get_autonomous_system_setting(request):
    """Retrieve the current ASN configuration of the user. """
    system = AutonomousSystem.get_asn_by_username("admin")
    if system is None:
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": "ASN configuration not found!", "autonomous_system": None}, status=404)
    return JsonResponse({"monitoring_possible": True, "host": system.name,
                         "message": "Success!", "autonomous_system": "ASN" + str(system.number)}, status=200)


@router.put("/{as_number}", response=AutonomousSystemSetting, tags=[TAG])
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
