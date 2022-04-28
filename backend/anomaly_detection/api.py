from django.http import JsonResponse
from ninja import Router

from anomaly_detection.monitor_manager import MonitorManager
from database.models import AutonomousSystem, MeasurementCollection

router = Router()


@router.get("/a", tags=["ASN"])
def koen(request):
    asn = 1103 #request.data.get('asn')

    asn_id = AutonomousSystem.objects.get(number=asn)

    measurements = MeasurementCollection.objects.get(autonomous_system=asn_id)
    monitor_manager = MonitorManager()
    monitor_manager.create_monitors(measurements)

    return JsonResponse({"message": "Monitoring Process started for the following ASN:" + str(asn)}, status=200)
