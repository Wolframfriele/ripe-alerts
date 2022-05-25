from ssl import create_default_context
from turtle import up
from urllib import response

from django.http import JsonResponse
from ninja import Router, Path, Query
from database.models import Feedback, Anomaly
from feedback.api_schema import FeedbackFormat, FeedbackOut

router = Router()
"""Tags are used by Swagger to group endpoints."""
TAG = "Feedback"


@router.put("/", response=FeedbackOut, tags=[TAG])  # TODO: Create documentation
def save_feedback(request, data: FeedbackFormat = Query(...)):
    anomaly_exist = Anomaly.objects.filter(id=data.anomaly_id).exists()
    if not anomaly_exist:
        return JsonResponse({"message": f"Failed, anomaly {data.anomaly_id} does not exists!"}, status=404)
    Feedback.create_or_update(data.anomaly_id, data.user_feedback)
    return JsonResponse({"message": f"The feedback for anomaly {data.anomaly_id} has been succesfully saved!"}, status=200)
