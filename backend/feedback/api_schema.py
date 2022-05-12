from pydantic import Field
from typing import Optional
from ninja import Schema

class FeedbackOut(Schema):
    anomaly_id: int = Field(1, description="The anomaly id the feedback was saved on!")
    feedback: Optional[bool] = Field(True, description="User feedback that has been saved in the database!")
    message: str = Field("Success!", description="Response from the server.")

class FeedbackFormat(Schema):
    anomaly_id: int = Field(1, description="The ID of the anomaly the feedback was on.")
    user_feedback: Optional[bool] = Field(True, description="User feedback, whether the prediction was accurate (True) or "
                                                       "not. (False)")
