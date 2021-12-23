from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlertConfiguration, Anomaly
from .serializers import AnomalySerializer
from users.models import  User
from django.core.exceptions import ObjectDoesNotExist
from .services import get_alerts, get_anomalies
import time


class AlertConfigurationList(APIView):
    """List of alert configurations"""

    def get(self, request):
        """ get all AlertConfigurations belonging to user"""
        user = request.user
        try:
            print(user.ripe_api_token.ripe_api_token)
        except ObjectDoesNotExist:
            print("has no ripe token")

        return AlertConfiguration.objects.all()

    def post(self, request):
        """ Add new alert configurations"""

        return Response(data=None, status=status.HTTP_201_CREATED)


class AlertList(APIView):
    def get(self, request):
        all_anomalies = int(request.query_params.get('all_anomalies', 1))
        item = int(request.query_params.get('item', 0))
        # wanneer gebruikers in het systeem zijn dan hoeft de user object niet gehardcode te worden
        user = User.objects.get(id=2)

        if all_anomalies == 1:
            anomalies = get_anomalies(user.id, item)
        else:
            anomalies = get_alerts(user.id, item)

        anomalies_serialized = AnomalySerializer(anomalies, many=True)
        return Response(anomalies_serialized.data, status=status.HTTP_200_OK)


class LabelAlert(APIView):

    def post(self, request):
        try:
            anomaly = Anomaly.objects.get(pk=request.data.get('anomaly_id'))
        except ObjectDoesNotExist:
            return Response("Anomaly_id does not exist in the database.", status=status.HTTP_404_NOT_FOUND)
        anomaly.label = request.data.get('label', None)
        anomaly.save()
        anomaly_serialized = AnomalySerializer(anomaly)
        return Response(anomaly_serialized.data, status=status.HTTP_200_OK)

