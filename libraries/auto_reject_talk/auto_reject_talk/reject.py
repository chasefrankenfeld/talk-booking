MAX_DURATION_IN_MINUTES = 90
MIN_DURATION_IN_MINUTES = 20


def process(talk_request):
    if not (
        MIN_DURATION_IN_MINUTES
        <= talk_request.duration_in_minutes
        <= MAX_DURATION_IN_MINUTES
    ):
        talk_request.reject()

    return talk_request
