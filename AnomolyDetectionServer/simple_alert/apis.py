from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .monitors import Measurement
from .monitor_manager import MonitorManager

monitor_manager = MonitorManager()


class CreateMonitor(APIView):

    def post(self, request):
        measurement_id = request.data.get('measurement_id')
        type = request.data.get('type')
        monitor_manager.create_monitor(Measurement(measurement_id, type))
        return Response(f"Measurement {measurement_id} is being monitored", status=status.HTTP_200_OK)
