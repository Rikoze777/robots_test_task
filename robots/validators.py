from pydantic import BaseModel, Field
from datetime import datetime


class RobotSchema(BaseModel):
    model: str = Field(..., max_length=2)
    version: str = Field(..., max_length=2)
    created: datetime
