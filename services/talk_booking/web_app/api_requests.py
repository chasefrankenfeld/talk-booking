import datetime

from pydantic import BaseModel, PositiveInt, EmailStr

from models import Address


class SubmitTalkRequest(BaseModel):
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
