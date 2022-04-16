from fastapi import FastAPI

from .api_requests import SubmitTalkRequest


# fast api app
app = FastAPI()


# health check for aws
@app.get("/health-check/")
def health_check():
    return {"message": "OK"}


@app.post("/request-talk/", status_code=201)
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
