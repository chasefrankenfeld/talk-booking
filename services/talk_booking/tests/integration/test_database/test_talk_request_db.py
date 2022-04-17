import datetime
import uuid

from database import talk_request_db
from models import Address, TalkRequest


def test_talk_request(database_session):
    """
    GIVEN talk request and database
    WHEN talk request is saved
    THEN in can accessed by its id or listed
    """
    talk_request = TalkRequest(
        id=str(uuid.uuid4()),
        event_time=datetime.datetime.utcnow(),
        address=Address(
            street="Sunny street 42",
            city="Awesome city",
            state="Best state",
            country="Ireland",
        ),
        duration_in_minutes=45,
        topic="Python type checking",
        requester="john@doe.com",
        status="PENDING",
    )

    talk_request_db.save(database_session, talk_request)

    assert talk_request_db.list_all(database_session)[0] == talk_request
    assert talk_request_db.get_by_id(database_session, talk_request.id) == talk_request
