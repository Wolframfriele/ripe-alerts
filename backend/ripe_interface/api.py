from typing import List

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from ninja import Router, Path
from ninja.pagination import paginate, PageNumberPagination

from database.models import AutonomousSystem, Setting, MeasurementCollection, Anomaly, MeasurementType, DetectionMethod
from ripe_interface.api_schemas import AutonomousSystemSetting, ASNumber, AutonomousSystemSetting2, AnomalyOut
from ripe_interface.ripe_requests import RipeRequests

anomaly_router = Router()
settings_router = Router()
"""Tags are used by Swagger to group endpoints."""
ANOMALIES_TAG = "Anomalies"
ASN_SETTINGS_TAG = "Settings"


def get_username(request):
    default_user = 'admin'
    if hasattr(request, 'auth'):
        return str(request.auth)
    else:
        return default_user


@anomaly_router.get("/generate-fake-anomalies", tags=[ANOMALIES_TAG])
def generate_fake_anomalies(request):
    """This endpoint is for testing purposes only! It adds fake anomalies to the database"""
    asn = ASNumber()
    asn.value = 1103
    response = set_autonomous_system_setting(request=None, asn=asn)
    if not response.status_code == 200:
        return JsonResponse({"message": response.get('message')}, status=response.status_code)
    user = User.objects.get(username=get_username(request))
    setting = Setting.objects.get(user=user)
    system = AutonomousSystem.objects.get(setting_id=setting.id)
    method = DetectionMethod.objects.create(type="ipv6 traceroute", description="a1 algorithm")
    method.save()
    Anomaly.objects.create(time=timezone.now(), ip_address="localhost, google.com", autonomous_system=system,
                           description="Ping above 100ms",
                           measurement_type=MeasurementType.TRACEROUTE, detection_method=method, mean_increase=2.1,
                           anomaly_score=4.0, prediction_value=False, asn=1402)
    return JsonResponse({"message": "Success!"}, status=200)


@anomaly_router.get("/", response=List[AnomalyOut], tags=[ANOMALIES_TAG])
@paginate(PageNumberPagination)
def list_anomalies(request):
    """Retrieves all anomalies by user from the database.  """
    username = get_username(request)
    system = AutonomousSystem.get_asn_by_username(username=username)
    anomalies = Anomaly.objects.filter(autonomous_system=system)
    if anomalies is None:
        return []
    return anomalies


@settings_router.get("/", response=AutonomousSystemSetting2, tags=[ASN_SETTINGS_TAG])
def get_autonomous_system_setting(request):
    """Retrieve the current ASN configuration of the user. """
    system = AutonomousSystem.get_asn_by_username("admin")
    if system is None:
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": "ASN configuration not found!", "autonomous_system": None}, status=404)
    return JsonResponse({"monitoring_possible": True, "host": system.name,
                         "message": "Success!", "autonomous_system": "ASN" + str(system.number)}, status=200)


@settings_router.put("/{as_number}", response=AutonomousSystemSetting, tags=[ASN_SETTINGS_TAG])
def set_autonomous_system_setting(request, asn: ASNumber = Path(...)):
    """To monitor a specific Autonomous System, we'll first need a valid Autonomous
    System Number (ASN). This endpoint validates and saves the ASN configuration in the database.  """
    asn_name = "ASN" + str(asn.value)
    username = get_username(request)
    if not RipeRequests.autonomous_system_exist(asn.value):
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": asn_name + " does not exist!"}, status=400)

    anchors = RipeRequests.get_anchors(asn.value)
    if len(anchors) == 0:
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": "There were no anchors found in " + asn_name},
                            status=400)

    asn_location = RipeRequests.get_company_name(asn.value)
    user_exists = User.objects.filter(username=username).exists()
    if not user_exists:
        return JsonResponse({"monitoring_possible": False, "host": asn_location,
                             "message:": "User '" + username + "' does not exist!"}, status=400)

    user = User.objects.get(username=username)
    setting = Setting.get_user_settings(username)
    if setting is None:
        return JsonResponse({"monitoring_possible": False, "host": asn_location,
                             "message:": "User '" + username + "' settings is missing!"}, status=400)

    autonomous_system = AutonomousSystem.register_asn(setting=setting, system_number=asn.value, location=asn_location)
    MeasurementCollection.delete_all_by_asn(system=autonomous_system)
    for anchor in anchors:
        measurements = RipeRequests.get_anchoring_measurements(anchor.ip_v4)
        for measurement in measurements:
            measurement.save_to_database(system=autonomous_system)
    return JsonResponse({"monitoring_possible": True, "host": asn_location, "message": "Success!"}, status=200)
