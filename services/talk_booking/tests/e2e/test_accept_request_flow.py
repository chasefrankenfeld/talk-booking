# import requests


# def test_accept_request_flow():
#     api_url = "https://development.beerlibrary.co"
#     talk_request = request_talk(api_url)
#     find_talk_request_in_list(api_url, talk_request)
#     talk_request = accept_talk_request(api_url, talk_request)
#     find_talk_request_in_list(api_url, talk_request)


# def request_talk(api_url):
#     response = requests.post(
#         f"{api_url}/request-talk/",
#         json={
#             "event_time": "2021-10-03T10:30:00",
#             "address": {
#                 "street": "Sunny street 42",
#                 "city": "Sunny city 42000",
#                 "state": "Sunny state",
#                 "country": "Sunny country",
#             },
#             "topic": "FastAPI with Pydantic",
#             "duration_in_minutes": 45,
#             "requester": "john@doe.com",
#         },
#     )
#     assert response.status_code == 201, "Something went wrong while requesting a talk."

#     return response.json()


# def find_talk_request_in_list(api_url, talk_request):
#     response = requests.get(
#         f"{api_url}/talk-requests/",
#     )
#     assert (
#         talk_request in response.json()["results"]
#     ), "Talk request not found in the list."


# def accept_talk_request(api_url, talk_request):
#     response = requests.post(
#         f"{api_url}/talk-request/accept/", json={"id": talk_request["id"]}
#     )
#     assert response.status_code == 200, "Something went wrong while accepting a talk."
#     talk_request = response.json()
#     assert talk_request["status"] == "ACCEPTED"
#     return talk_request
