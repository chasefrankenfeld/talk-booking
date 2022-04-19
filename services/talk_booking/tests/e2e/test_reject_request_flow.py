import requests


def test_reject_request_flow():
    api_url = "https://development.your-domain.com"
    talk_request = request_talk(api_url)
    find_talk_request_in_list(api_url, talk_request)
    talk_request = reject_talk_request(api_url, talk_request)
    find_talk_request_in_list(api_url, talk_request)


def request_talk(api_url):
    response = requests.post(
        f"{api_url}/request-talk/",
        json={
            "event_time": "2021-10-03T10:30:00",
            "address": {
                "street": "Sunny street 42",
                "city": "Sunny city 42000",
                "state": "Sunny state",
                "country": "Sunny country",
            },
            "topic": "Complete Python toolbox",
            "duration_in_minutes": 45,
            "requester": "john@doe.com",
        },
    )
    assert response.status_code == 201, "Something went wrong while requesting a talk."

    return response.json()


def find_talk_request_in_list(api_url, talk_request):
    response = requests.get(f"{api_url}/talk-requests/",)
    assert (
        talk_request in response.json()["results"]
    ), "Talk request not found in the list."


def reject_talk_request(api_url, talk_request):
    response = requests.post(
        f"{api_url}/talk-request/reject/", json={"id": talk_request["id"]}
    )
    assert response.status_code == 200, "Something went wrong while rejecting a talk."
    talk_request = response.json()
    assert talk_request["status"] == "REJECTED"
    return talk_request
