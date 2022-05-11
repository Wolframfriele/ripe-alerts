from pydantic import Field
from typing import Optional
from ninja import Schema

class FeedbackFormat(Schema):
    anomaly_id: int = Field(1, description="The ID of the anomaly the feedback was on.")
    feedback: Optional[bool] = Field(True, description="User feedback, whether the prediction was accurate (True) or "
                                                       "not. (False)")