import datetime

from models import Address, TalkRequest


def test_talk_request_attributes():
    """
    GIVEN id, event time, address, duration in minutes, topic, requester, status
    WHEN TalkRequest is initialized
    THEN it has attributes with the same values as provided
    """
    event_time = datetime.datetime.utcnow()
    talk_request = TalkRequest(
        id="request_id",
        event_time=event_time,
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

    assert talk_request.id == "request_id"
    assert talk_request.event_time == event_time
    assert talk_request.address == Address(
        street="Sunny street 42",
        city="Awesome city",
        state="Best state",
        country="Ireland",
    )

    assert talk_request.duration_in_minutes == 45
    assert talk_request.topic == "Python type checking"
    assert talk_request.requester == "john@doe.com"
    assert talk_request.status == "PENDING"


def test_talk_request_accept():
    """
    GIVEN talk_request
    WHEN accept is called
    THEN status is set to ACCEPTED
    """
    event_time = datetime.datetime.utcnow()
    talk_request = TalkRequest(
        id="request_id",
        event_time=event_time,
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

    talk_request.accept()

    assert talk_request.status == "ACCEPTED"


def test_reject_talk_request(client, database_session):
    """
    GIVEN id of talk request
    WHEN reject talk request endpoint is called
    THEN request is rejected
    """
    talk_request = TalkRequest(
        id=str(uuid.uuid4()),
        event_time="2021-10-03T10:30:00",
        address=Address(
            street="Sunny street 42",
            city="Sunny city 42000",
            state="Sunny state",
            country="Sunny country",
        ),
        duration_in_minutes=45,
        topic="FastAPI with Pydantic",
        requester="john@doe.com",
        status="PENDING",
    )
    talk_request_db.save(database_session, talk_request)
    response = client.post(
        "/talk-request/reject/",
        json={"id": talk_request.id},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == talk_request.id
    assert response_body["status"] == "REJECTED"
