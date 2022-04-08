from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Schema, Path
from ninja.security import django_auth
from pydantic import Field

from database.models import AutonomousSystem, Setting
from ripe_interface.requests import RipeRequests

router = Router()
"""Tags are used by Swagger to group endpoints."""
TAG = "Ripe Interface"


class AutonomousSystemSetting(Schema):
    monitor_possible: bool = Field(True, alias="Whether it is possible or not to monitor the given autonomous system.")
    host: str = Field("VODANET - Vodafone GmbH", alias="Hostname of the autonomous system.")
    message: str = Field("Success!", alias="Response from the server.")


class ASNumber(Schema):
    value: int = Field(1103, alias="as_number", description="The Autonomous system number to be set for the user for "
                                                            "monitoring. ")


@router.get("/{as_number}", response=AutonomousSystemSetting, tags=[TAG])
def set_autonomous_system_setting(request, asn: ASNumber = Path(...)):
    asn_name = "ASN" + str(asn.value)
    if not RipeRequests.autonomous_system_exist(asn.value):
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": asn_name + " does not exist!"}, status=404)

    anchors = RipeRequests.get_anchors(asn.value)
    if len(anchors) == 0:
        return JsonResponse({"monitoring_possible": False, "host": None,
                             "message": "There were no anchors found in " + asn_name}, status=404) #TODO: all edit status code except for the last one200

    asn_location = anchors[0].company + " - " + anchors[0].country
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
    autonomous_system_registered = AutonomousSystem.objects.filter(setting_id=setting.id).exists()
    if not autonomous_system_registered:
        AutonomousSystem.objects.create(setting=setting, number=asn.value, name=asn_location)
    elif autonomous_system_registered:
        autonomous_system = AutonomousSystem.objects.get(setting_id=setting.id)
        autonomous_system.number = asn.value
        autonomous_system.name = asn_location
        autonomous_system.save()

    for x in anchors:
        measurements = RipeRequests.get_anchoring_measurements(x.ip_v4)
        # for y in measurements:
    # print(RipeRequests.get_anchoring_measurements(anchors[0].ip_v4))
    return JsonResponse({"monitoring_possible": True, "host": asn_location, "message": "Success!"}, status=200)


# POST AS Nummer, output. Kan het gebruikt worden om te monitoren.
# GET
@router.get("/pets", tags=[TAG], auth=django_auth)
def pets(request):
    if request.user.is_authenticated():
        username = request.user.username
        return JsonResponse({'username': request.user.username})
    return JsonResponse({'username': "nope"})
    # return f"Authenticated user {request.auth}"

    # def my_view(request):
    #     username = None
    #     if request.user.is_authenticated():
    #         username = request.user.username


@router.get('/{event_id}', tags=[TAG])
def event_details(request, event_id: int):
    return {"title": event_id, "details": "not for now!"}
