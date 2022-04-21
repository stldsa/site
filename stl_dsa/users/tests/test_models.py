from stl_dsa.users.models import User
import actionnetwork.action_network as an
import responses
from responses import matchers
import pytest


# def test_new_user_is_not_member(mocker):
#     # Taggings.has_tag() should return false since the new user has no tags
#     mocker.patch("stl_dsa.users.models.Taggings.has_tag", return_value=False)
#     # User.taggings() should return a taggings object with a test_uuid
#     test_uuid = "a123"
#     taggings_response = an.Taggings(test_uuid)
#     mocker.patch.object(User, "taggings", taggings_response)
#     # People.from_email() should return JSON of the form that we expect
#     new_people = {"_links": {"osdi:people": []}}
#     from_email_response = People(new_people)
#     mocker.patch.object(People, "from_email", from_email_response)

#     assert User().is_member is False
#     # assert mocker.called  # This stopped working?


@pytest.mark.django_db
@responses.activate
def test_existing_user_is_member(faker):
    uuid = faker.uuid4()
    voting_tag_uuid = faker.uuid4()
    assert uuid != voting_tag_uuid
    url = "https://actionnetwork.org/api/v2/people"
    responses.add(
        responses.GET,
        url=url,
        match=[
            matchers.query_param_matcher(
                {"filter": "email_address eq 'member@example.com'"}
            )
        ],
        json={"_links": {"osdi:people": [{"href": f"{url}/{uuid}"}]}},
    )
    responses.add(
        responses.GET,
        url=f"{url}/{uuid}/taggings",
        json={
            "_embedded": {
                "osdi:taggings": [
                    {
                        "_links": {
                            "osdi:tag": {
                                "href": f"https://actionnetwork.org/api/v2/tags/{voting_tag_uuid}"
                            }
                        }
                    }
                ]
            }
        },
    )
    assert voting_tag_uuid in an.Taggings(uuid).tags


@pytest.mark.django_db
@responses.activate
def test_get_uuid_when_doesnt_have_one(faker):
    uuid = faker.uuid4()
    email = faker.email()
    url = "https://actionnetwork.org/api/v2/people"
    responses.add(
        responses.GET,
        url=url,
        match=[matchers.query_param_matcher({"filter": f"email_address eq '{email}'"})],
        json={"_links": {"osdi:people": [{"href": f"{url}/{uuid}"}]}},
    )

    assert User(email=email).get_uuid() == uuid
