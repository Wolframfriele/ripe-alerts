from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .monitor_manager import MonitorManager
from .services import get_measurementcollection_by_asn
from database.models import MeasurementCollection, AutonomousSystem

# monitor_manager = MonitorManager()


class MonitorProcess(APIView):

    def post(self, request):
        asn = request.data.get('asn')
        asn_id = AutonomousSystem.objects.get(number=asn)

        print(0)
        measurements = MeasurementCollection.objects.get(autonomous_system=asn_id)
        print('1')
        print(measurements)
        monitor_manager.create_monitors(measurements)

        return Response(f"Monitoring Process started for the following asns: {asn}", status=status.HTTP_201_CREATED)


class Feedback(APIView):

    def post(self, request):
        monitor_id = request.data.get('id')
        monitor_manager.monitors[monitor_id].restart()
        return Response("Feedback has been processed", status=status.HTTP_200_OK)
