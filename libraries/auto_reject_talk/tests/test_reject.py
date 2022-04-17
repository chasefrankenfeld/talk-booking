import auto_reject_talk


def test_process():
    """
    GIVEN request talk with duration in munites
    WHEN process is called
    THEN talk is rejected if the duration is longer than 90min or shorter than 20min
    """

    class TalkRequest:
        def __init__(self, status, duration_in_minutes):
            self.duration_in_minutes = duration_in_minutes
            self.status = status

        def reject(self):
            self.status = "REJECTED"

    processed_request = auto_reject_talk.process(TalkRequest("PENDING", 45))
    assert processed_request.status == "PENDING"

    processed_request = auto_reject_talk.process(TalkRequest("PENDING", 15))
    assert processed_request.status == "REJECTED"

    processed_request = auto_reject_talk.process(TalkRequest("PENDING", 120))
    assert processed_request.status == "REJECTED"
