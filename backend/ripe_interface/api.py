from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.security import django_auth
from pydantic import Field

from database.models import AutonomousSystem, Setting
from ripe_interface.requests import RipeRequests

router = Router()
"""Tags are used by Swagger to group endpoints."""
TAG = "Ripe Interface"


class AutonomousSystemSetting(Schema):
    monitor_possible: bool = Field(None, alias="Whether it is possible or not to monitor the given autonomous system.")
    hostname: str = Field(None, alias="Hostname of the autonomous system.")


@router.get("/{as_number}", response=AutonomousSystemSetting, tags=[TAG])
def set_autonomous_system_setting(request, as_number: int):
    anchors = RipeRequests.get_anchors(as_number)
    if len(anchors) == 0:
        return JsonResponse({"monitoring_possible": False, "hostname": None}, status=200)
    else:
        as_name = anchors[0].company + " - " + anchors[0].country
        user = get_object_or_404(User, username="admin")
        if user is None:
            return JsonResponse({"message:": "User 'admin' not found!"}, status=400)
        else:
            setting = Setting.objects.create(user=user)
            setting.save()

            JsonResponse({"monitoring_possible": True, "hostname": None}, status=200)
            print(as_name)

        # asn = AutonomousSystem(number=anchors[0].ip_v4, name=)
        # autonomous_system = AutonomousSystem.objects.create()
        return {"amount of anchors: ": len(anchors)}


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
