from fastapi import FastAPI

from .requests import SubmitTalkRequest, AcceptTalkRequest
from .responses import TalkRequestDetails, TalkRequestList


# fast api app
app = FastAPI()


# health check for aws
@app.get("/health-check/")
def health_check():
    return {"message": "OK"}


@app.post("/request-talk/", status_code=201, response_model=TalkRequestDetails)
def request_talk(submit_talk_request: SubmitTalkRequest):
    return {
        "id": "unique_id",
        "event_time": submit_talk_request.event_time,
        "address": submit_talk_request.address,
        "topic": submit_talk_request.topic,
        "status": "PENDING",
        "duration_in_minutes": submit_talk_request.duration_in_minutes,
        "requester": submit_talk_request.requester,
    }


@app.get("/talk-requests/", status_code=200, response_model=TalkRequestList)
def talk_requests():
    return {
            "results": [
                {
                    "id": "unique_id",
                    "event_time": "2021-10-03T10:30:00",
                    "address": {
                        "street": "Sunny street 42",
                        "city": "Sunny city 42000",
                        "state": "Sunny state",
                        "country": "Sunny country",
                    },
                    "topic": "FastAPI with Pydantic",
                    "status": "PENDING",
                    "duration_in_minutes": 45,
                    "requester": "john@doe.com",
                }
            ]
        }


@app.post("/talk-request/accept/", status_code=200, response_model=TalkRequestDetails)
def accept_talk_request(accept_talk_request_body: AcceptTalkRequest):
    return {
        "id": accept_talk_request_body.id,
        "event_time": "2021-10-03T10:30:00",
        "address": {
            "street": "Sunny street 42",
            "city": "Sunny city 42000",
            "state": "Sunny state",
            "country": "Sunny country",
        },
        "topic": "FastAPI with Pydantic",
        "status": "ACCEPTED",
        "duration_in_minutes": 45,
        "requester": "john@doe.com",
    }
