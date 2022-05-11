from ninja import Router
from database.models import Feedback
from feedback.api_schema import FeedbackFormat

router = Router()
"""Tags are used by Swagger to group endpoints."""
TAG = "Feedback"

@router.post("/feedback", tags=[TAG]) #TODO: Create documentation
def save_feedback(request, feedback:FeedbackFormat):
    feedback_save = Feedback.objects.create(anomaly_id=feedback.anomaly_id, response=feedback.feedback)
    feedback_save.save()
    return "Feedback has been saved succesfully!"