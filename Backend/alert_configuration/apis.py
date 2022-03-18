from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Anomaly, Feedback
from .serializers import AnomalySerializer
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
from .services import get_alerts, get_anomalies


class AlertList(APIView):
    """Returns a list of all alerts or anomalies that have been detected"""

    def get(self, request):
        all_anomalies = int(request.query_params.get('all_anomalies', 1))
        item = int(request.query_params.get('item', 0))

        # since we dont have an authentication system on the frontend we use a default user
        user = User.objects.get(id=1)

        if all_anomalies == 1:
            anomalies = get_anomalies(user.id, item)
        else:
            anomalies = get_alerts(user.id, item)

        anomalies_serialized = AnomalySerializer(anomalies, many=True)
        return Response(anomalies_serialized.data, status=status.HTTP_200_OK)


class LabelAlert(APIView):
    """Label the alerts and anomalies that have been detected"""

    def post(self, request):
        try:
            anomaly = Anomaly.objects.get(pk=request.data.get('anomaly_id'))
        except ObjectDoesNotExist:
            return Response("Anomaly_id does not exist in the database.", status=status.HTTP_404_NOT_FOUND)
        anomaly.label = request.data.get('label', None)
        anomaly.save()
        anomaly_serialized = AnomalySerializer(anomaly)
        return Response(anomaly_serialized.data, status=status.HTTP_200_OK)


class FeedBack(APIView):
    "Saving the feedback to the database"

    def post(self, request):
        anomaly_id = request.data.get("anomaly_id")
        response = request.data.get("response")

        anomaly = Anomaly.objects.get(id=anomaly_id)

        feedback = Feedback(anomaly_id=anomaly, response=response)
        feedback.save()

        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        anomaly_id = request.data.get("anomaly_id")
        response = request.data.get("response")

        feedback_data = Feedback.objects.get(anomaly_id=anomaly_id)
        feedback_data.response = response

        feedback_data.save(update_fields=['response'])

        return Response(status=status.HTTP_200_OK)
