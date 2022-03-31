from ninja import Router
from ninja.security import django_auth

from database.models import AutonomousSystem
from ripe_interface.constants import TAG_WEB as TAG
from ripe_interface.requests import RipeRequests

router = Router()


@router.get("/{as_number}", tags=[TAG])
def set_autonomous_system_setting(request, as_number: int):
    anchors = RipeRequests.get_anchors(as_number)
    if len(anchors) == 0:
        return {"monitoring_possible": False, "hostname": None}
    else:
        as_name = anchors[0].company + " - " + anchors[0].country
        print(as_name)
        # asn = AutonomousSystem(number=anchors[0].ip_v4, name=)
        # autonomous_system = AutonomousSystem.objects.create()
        return {"amount of anchors: ": len(anchors)}


# POST AS Nummer, output. Kan het gebruikt worden om te monitoren.
# GET
@router.get("/pets", tags=[TAG], auth=django_auth)
def pets(request):
    return f"Authenticated user {request.auth}"


@router.get('/{event_id}', tags=[TAG])
def event_details(request, event_id: int):
    return {"title": event_id, "details": "not for now!"}
