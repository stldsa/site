from actionnetwork import action_network as an
from faker import Faker
import responses

fake = Faker()


@responses.activate
def test_call_api(faker):
    url = faker.url()
    email = faker.email()
    responses.add(responses.GET, url + f"?filter=email_address eq '{email}'", json={})
    an.call_api(url, params={"filter": f"email_address eq '{email}'"})


def test_people_from_email(faker, monkeypatch):
    email = faker.email()
    monkeypatch.setattr(
        an,
        "call_api",
        lambda self, params=None: {
            "_links": {"osdi:people": [{"href": faker.uuid4()}]}
        },
    )
    assert an.People.from_email(email)


def test_taggings_has_tag(monkeypatch, faker):
    voting_member_tag_id = faker.uuid4()
    monkeypatch.setattr(an.Taggings, "tags", [voting_member_tag_id])
    taggings = an.Taggings({})
    assert taggings.has_tag(voting_member_tag_id)


def test_uuid(faker):
    uuid = faker.uuid4()
    assert an.Person({"identifiers": ["action_network:" + uuid]}).uuid == uuid


def test_people_json():
    assert an.People({}).json == {}


def test_tag_json():
    assert an.Tag({}).json == {}


def test_get_tag_from_uuid(faker, monkeypatch):
    uuid = faker.uuid4()
    monkeypatch.setattr(
        an, "call_api", lambda uri: {"identifiers": ["action_network:" + uuid]}
    )
    tag = an.Tag.from_uuid(uuid).json
    assert tag["identifiers"][0].split(":")[1] == uuid
