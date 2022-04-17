import uuid

from database import talk_request_db
from models import Address, TalkRequest


def test_health_check(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/health-check/")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def test_request_talk(client):
    """
    GIVEN event time, address, topic, duration in minutes, requester
    WHEN request talk endpoint is called
    THEN request talk with the same attributes as provided is returned
    """
    response = client.post(
        "/request-talk/",
        json={
            "event_time": "2021-10-03T10:30:00",
            "address": {
                "street": "Sunny street 42",
                "city": "Sunny city 42000",
                "state": "Sunny state",
                "country": "Sunny country",
            },
            "topic": "FastAPI with Pydantic",
            "duration_in_minutes": 45,
            "requester": "john@doe.com",
        },
    )
    assert response.status_code == 201
    response_body = response.json()
    assert isinstance(response_body["id"], str)
    assert response_body["event_time"] == "2021-10-03T10:30:00"
    assert response_body["address"] == {
        "street": "Sunny street 42",
        "city": "Sunny city 42000",
        "state": "Sunny state",
        "country": "Sunny country",
    }
    assert response_body["topic"] == "FastAPI with Pydantic"
    assert response_body["status"] == "PENDING"
    assert response_body["duration_in_minutes"] == 45
    assert response_body["requester"] == "john@doe.com"


def test_list_requests(client, database_session):
    """
    GIVEN
    WHEN list requests endpoint is called
    THEN list of requests is returned
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

    # need to change this to getting the item with the same ID
    response = client.get(
        "/talk-requests/",
    )
    assert response.status_code == 200

    response_body = response.json()

    talk_requests = response_body["results"]
    assert isinstance(talk_requests[1]["id"], str)
    assert talk_requests[1]["event_time"] == "2021-10-03T10:30:00"
    assert talk_requests[1]["address"] == {
        "street": "Sunny street 42",
        "city": "Sunny city 42000",
        "state": "Sunny state",
        "country": "Sunny country",
    }
    assert talk_requests[1]["topic"] == "FastAPI with Pydantic"
    assert talk_requests[1]["status"] == "PENDING"
    assert talk_requests[1]["duration_in_minutes"] == 45
    assert talk_requests[1]["requester"] == "john@doe.com"


def test_accept_talk_request(client, database_session):
    """
    GIVEN id of talk request
    WHEN accept talk request endpoint is called
    THEN request is accepted
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
        "/talk-request/accept/",
        json={"id": talk_request.id},
    )
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == talk_request.id
    assert response_body["status"] == "ACCEPTED"


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
