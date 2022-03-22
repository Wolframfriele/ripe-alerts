from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .monitor_manager import MonitorManager
from .services import get_alert_configurations_by_asn

monitor_manager = MonitorManager()


class MonitorProcess(APIView):

    def post(self, request):
        asns = request.data.get('asns')
        for asn in asns:
            alert_configurations = get_alert_configurations_by_asn(asn)
            monitor_manager.create_monitors(alert_configurations)
        return Response(f"Monitoring Process started for the following asns: {asns}", status=status.HTTP_201_CREATED)


class Feedback(APIView):

    def post(self, request):
        monitor_id = request.data.get('id')
        monitor_manager.monitors[monitor_id].restart()
        return Response("Feedback has been processed", status=status.HTTP_200_OK)
