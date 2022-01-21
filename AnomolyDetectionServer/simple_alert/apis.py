from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .monitor_manager import MonitorManager
from .services import get_measurements

monitor_manager = MonitorManager()


class MonitorProcess(APIView):

    def post(self, request):
        asns = request.data.get('asns')
        for asn in asns:
            measurements = get_measurements(asn)
            for measurement in measurements:
                monitor_manager.create_monitor(measurement)
        return Response(f"Monitoring Process started for the following asns: {asns}", status=status.HTTP_201_CREATED)


class Feedback(APIView):

    def post(self, request):
        monitor_id = request.data.get('id')
        monitor_manager.monitors[monitor_id].restart()
        return Response("Feedback has been processed", status=status.HTTP_200_OK)
