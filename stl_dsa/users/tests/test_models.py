from stl_dsa.users.models import User
import actionnetwork.action_network as an


def test_new_user_is_member(monkeypatch, faker):
    monkeypatch.setattr(User, "get_uuid", faker.uuid4)
    monkeypatch.setattr(an.Taggings, "has_tag", lambda self, tag: True)
    assert User(email=faker.email()).is_member


def test_existing_user_is_member(monkeypatch, faker):
    monkeypatch.setattr(an.Taggings, "has_tag", lambda self, tag: True)
    assert User(uuid=faker.uuid4()).is_member


def test_get_uuid_already_has_one(faker):
    uuid = faker.uuid4()
    user = User(email=faker.email(), uuid=uuid)
    user.get_uuid()
    assert user.uuid == uuid


def test_get_uuid_when_doesnt_have_one(faker, monkeypatch):
    uuid = faker.uuid4()
    user = User(email=faker.email())
    monkeypatch.setattr(an.Person, "from_email", lambda email: an.Person({}))
    monkeypatch.setattr(an.Person, "uuid", uuid)

    assert user.get_uuid() == uuid
