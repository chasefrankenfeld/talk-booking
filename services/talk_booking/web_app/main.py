# import pathlib
import uuid
from typing import Generator

from fastapi import Depends, FastAPI, Response
# from sqlalchemy import create_engine

# from alembic import config, script
# from alembic.runtime import migration
from database import talk_request_db
from database.session import SessionLocal
from models import TalkRequest

from .config import load_config
from .requests import AcceptTalkRequest, RejectTalkRequest, SubmitTalkRequest
from .responses import TalkRequestDetails, TalkRequestList

# fast api app
app = FastAPI()
app_config = load_config()


# set up db session
def get_db_session() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# health check for aws
@app.get("/health-check/")
def health_check(response: Response):
    # engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
    # alembic_cfg = config.Config()
    # alembic_cfg.set_main_option(
    #     "script_location",
    #     str(pathlib.Path(__file__).parent.parent.absolute() / "alembic"),
    # )
    # db_script = script.ScriptDirectory.from_config(alembic_cfg)
    # with engine.begin() as conn:
    #     context = migration.MigrationContext.configure(conn)
    #     if context.get_current_revision() != db_script.get_current_head():
    #         response.status_code = 400
    #         return {"message": "Upgrade the database."}

    return {"message": "OK"}


@app.post("/request-talk/", status_code=201, response_model=TalkRequestDetails)
def request_talk(
    submit_talk_request: SubmitTalkRequest, db_session=Depends(get_db_session)
):
    talk_request = TalkRequest(
        id=str(uuid.uuid4()),
        event_time=submit_talk_request.event_time,
        address=submit_talk_request.address,
        topic=submit_talk_request.topic,
        status="PENDING",
        duration_in_minutes=submit_talk_request.duration_in_minutes,
        requester=submit_talk_request.requester,
    )
    talk_request = talk_request_db.save(db_session, talk_request)
    return talk_request


@app.get("/talk-requests/", status_code=200, response_model=TalkRequestList)
def talk_requests(db_session=Depends(get_db_session)):
    return {
        "results": [
            talk_request.dict() for talk_request in talk_request_db.list_all(db_session)
        ]
    }


@app.post("/talk-request/accept/", status_code=200, response_model=TalkRequestDetails)
def accept_talk_request(
    accept_talk_request_body: AcceptTalkRequest, db_session=Depends(get_db_session)
):
    talk_request = talk_request_db.get_by_id(db_session, accept_talk_request_body.id)
    talk_request.accept()
    talk_request = talk_request_db.save(db_session, talk_request)

    return talk_request


@app.post("/talk-request/reject/", status_code=200, response_model=TalkRequestDetails)
def reject_talk_request(
    reject_talk_request_body: RejectTalkRequest, db_session=Depends(get_db_session)
):
    talk_request = talk_request_db.get_by_id(db_session, reject_talk_request_body.id)
    talk_request.reject()
    talk_request = talk_request_db.save(db_session, talk_request)

    return talk_request
