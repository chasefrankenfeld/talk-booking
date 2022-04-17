from sqlalchemy import JSON, Column, DateTime, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base

from models import TalkRequest

TalkRequestBase = declarative_base()


class TalkRequestModel(TalkRequestBase):
    __tablename__ = "talk_request"

    id = Column(String(36), primary_key=True, index=True, nullable=False)
    event_time = Column(DateTime(), nullable=True)
    address = Column(JSON, nullable=False)
    topic = Column(String(), nullable=False)
    duration_in_minutes = Column(SmallInteger(), nullable=False)
    requester = Column(String(120), nullable=False)
    status = Column(String(20), nullable=False)


def save(session, talk_request):
    talk_request_model = TalkRequestModel(
        id=talk_request.id,
        event_time=talk_request.event_time,
        address=talk_request.address.dict(),
        topic=talk_request.topic,
        duration_in_minutes=talk_request.duration_in_minutes,
        requester=talk_request.requester,
        status=talk_request.status,
    )
    session.merge(talk_request_model)
    session.commit()

    return talk_request


def list_all(session):
    records = session.query(TalkRequestModel).all()

    return [
        TalkRequest(
            id=record.id,
            event_time=record.event_time,
            address=record.address,
            topic=record.topic,
            duration_in_minutes=record.duration_in_minutes,
            requester=record.requester,
            status=record.status,
        )
        for record in records
    ]


def get_by_id(session, talk_request_id):
    record = (
        session.query(TalkRequestModel)
        .filter(TalkRequestModel.id == talk_request_id)
        .first()
    )

    return TalkRequest(
        id=record.id,
        event_time=record.event_time,
        address=record.address,
        topic=record.topic,
        duration_in_minutes=record.duration_in_minutes,
        requester=record.requester,
        status=record.status,
    )
