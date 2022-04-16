import datetime
from typing import List

from pydantic import BaseModel, EmailStr, PositiveInt

from models import Address
from models.talk_request import TalkRequestStatus


class TalkRequestDetails(BaseModel):
    id: str
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
    status: TalkRequestStatus


class TalkRequestList(BaseModel):
    results: List[TalkRequestDetails]
