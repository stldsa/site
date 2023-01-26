import responses
from responses import matchers

from stl_dsa.users.models import User


@responses.activate
def test_user_is_member(faker):
    uuid = faker.uuid4()
    user = User(uuid=uuid)
    responses.add(
        responses.GET,
        url=f"https://actionnetwork.org/api/v2/people/{uuid}",
        json={"custom_fields": {"actionkit_is_member_in_good_standing": "True"}},
    )
    assert user.is_member


@responses.activate
def test_user_is_not_member(faker):
    uuid = faker.uuid4()
    user = User(uuid=uuid)
    responses.add(
        responses.GET,
        url=f"https://actionnetwork.org/api/v2/people/{uuid}",
        json={"custom_fields": {"actionkit_is_member_in_good_standing": "False"}},
    )
    assert not user.is_member


@responses.activate
def test_nonexistent_an_person_is_member(faker):
    uuid = faker.uuid4()
    user = User(uuid=uuid)
    responses.add(
        responses.GET,
        url=f"https://actionnetwork.org/api/v2/people/{uuid}",
        json={},
    )
    assert not user.is_member


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

    # assert User(email=email).get_uuid() == uuid
