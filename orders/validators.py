from pydantic import BaseModel, EmailStr, Field


class OrderSchema(BaseModel):
    robot_serial: str = Field(..., max_length=5)
    customer: EmailStr
