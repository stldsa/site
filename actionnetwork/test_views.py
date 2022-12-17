# import responses

# from actionnetwork import views


# @responses.activate
# def test_person_helper(rf):
#     url = "https://actionnetwork.org/api/v2/people/"
#     request = rf.post(url, {"email": "test@example.com", "zip": "63118"})
#     responses.add(
#         responses.post(
#             url=url,
#             status=200,
#             json={
#                 "person": {
#                     "postal_addresses": [{"postal_code": request.POST.get("zip")}],
#                     "email_addresses": [{"address": request.POST.get("email")}],
#                     "status": "subscribed",
#                 }
#             },
#         )
#     )
#     response = views.person_helper(request)
#     assert response.status_code == 200
