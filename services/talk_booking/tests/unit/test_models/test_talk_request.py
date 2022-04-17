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
