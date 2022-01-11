from stl_dsa.users.models import User, VOTING_MEMBER_TAG_ID
import actionnetwork.action_network as an


def test_new_user_is_member(faker, monkeypatch):
    monkeypatch.setattr(User, "taggings", an.Taggings(faker.uuid4()))
    monkeypatch.setattr(
        an.Taggings,
        "has_tag",
        lambda self, tag: False,
    )
    assert User().is_member == False


def test_existing_user_is_member(monkeypatch, faker):
    monkeypatch.setattr(an.Taggings, "has_tag", lambda self, tag: True)
    assert User(uuid=faker.uuid4()).is_member


def test_get_uuid_when_doesnt_have_one(faker, monkeypatch):
    uuid = faker.uuid4()
    user = User(email=faker.email())
    monkeypatch.setattr(
        User,
        "get_primary_person",
        an.Person({"identifiers": ["action_network:" + uuid]}),
    )

    assert user.get_uuid() == uuid
