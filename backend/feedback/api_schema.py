from pydantic import Field
from typing import Optional
from ninja import Schema

class FeedbackOut(Schema):
    message: str = Field("The feedback for anomaly {anomaly_id} has been succesfully saved!", description="Response from the server.")

class FeedbackFormat(Schema):
    anomaly_id: int = Field(1, description="The ID of the anomaly the feedback was on.")
    user_feedback: Optional[bool] = Field(None, description="User feedback, whether the prediction was accurate (True) or "
                                                       "not. (False)")
