from ssl import create_default_context
from turtle import up
from urllib import response
from ninja import Router, Path
from database.models import Feedback
from feedback.api_schema import FeedbackFormat, FeedbackOut

router = Router()
"""Tags are used by Swagger to group endpoints."""
TAG = "Feedback"

@router.put("/feedback", response=FeedbackOut, tags=[TAG]) #TODO: Create documentation
def save_feedback(request, data: FeedbackFormat = Path(...)):
    print(data)
    Feedback.create_or_update(data.anomaly_id, data.user_feedback)
    # feedback, created = Feedback.objects.get_or_create(anomaly_id=data.anomaly_id, response=data.user_feedback)
    # print(feedback)
    # print(created)
    # if not created:
    #     print('updating data')
    #     feedback = Feedback.objects.filter(anomaly_id=data.anomaly_id).update(response=data.user_feedback)
    #     print(feedback)
    return "Feedback has been saved succesfully!"