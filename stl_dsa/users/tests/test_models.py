from stl_dsa.users.models import User, Taggings
import actionnetwork.action_network as an
from actionnetwork.action_network import People
import responses


def test_new_user_is_not_member(mocker):
    # Taggings.has_tag() should return false since the new user has no tags
    mocker.patch("stl_dsa.users.models.Taggings.has_tag", return_value=False)
    # User.taggings() should return a taggings object with a test_uuid
    test_uuid = "a123"
    taggings_response = Taggings(test_uuid)
    mocker.patch.object(User, "taggings", taggings_response)
    # People.from_email() should return JSON of the form that we expect
    new_people = {"_links": {"osdi:people": []}}
    from_email_response = People(new_people)
    mocker.patch.object(People, "from_email", from_email_response)

    assert User().is_member is False
    # assert mocker.called  # This stopped working?


def test_existing_user_is_member(monkeypatch, faker):
    monkeypatch.setattr(an.Taggings, "has_tag", lambda self, tag: True)
    assert User(uuid=faker.uuid4()).is_member


# @responses.activate
# def test_get_uuid_when_doesnt_have_one(faker, people_endpoint):
#     uuid = faker.uuid4()
#     responses.add(responses.GET, url=f'{people_endpoint}/{uuid}', json={})
#     user = User(email=faker.email())

#     assert user.get_uuid() == uuid
