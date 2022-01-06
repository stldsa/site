from actionnetwork import action_network as an
import pytest
import requests
import responses
from faker import Faker

fake = Faker()

# def test_events_resource():
#     events = an.Resource("events", "main").list
#     assert len(events) > 1


# def test_person_resource():
#     id = fake.uuid4()
#     an.Resource("people", group="main", id=id)


@pytest.fixture
def member_uuid(faker):
    return faker.uuid4()


@pytest.fixture
def nonmember_uuid(faker):
    return faker.uuid4()


@pytest.fixture
def nonmember_taggings_response():
    return [
        {
            "_links": {
                "osdi:tag": {"href": "https://actionnetwork.org/api/v2/tags/random_tag"}
            }
        }
    ]


@pytest.fixture
def nonmember_person_response(nonmember_uuid):
    return {
        "_embedded": {
            "osdi:people": [
                {
                    "_links": {
                        "osdi:taggings": {
                            "href": f"https://actionnetwork.org/api/v2/people/{nonmember_uuid}/taggings"
                        }
                    }
                }
            ]
        }
    }


@pytest.fixture
def member_person_response(member_uuid):
    return {
        "_embedded": {
            "osdi:people": [
                {
                    "_links": {
                        "osdi:taggings": {
                            "href": f"https://actionnetwork.org/api/v2/people/{member_uuid}/taggings"
                        }
                    }
                }
            ]
        }
    }


def test_get_taggings_href():
    url = fake.url()
    tag_json = {"osdi:taggings": {"href": url}}
    assert an.get_resource_href(tag_json, "taggings") == url


def test_get_person_hrefs_from_taggings():
    url1 = fake.url()
    url2 = fake.url()
    taggings = [
        {"osdi:people": {"href": url1}},
        {"osdi:people": {"href": url2}},
    ]
    assert an.get_resources_hrefs(taggings, "people") == [url1, url2]


def test_get_emails_from_people_resources():
    email1 = fake.email()
    email2 = fake.email()
    resources = [
        {"email_addresses": [{"address": email1}]},
        {"email_addresses": [{"address": email2}]},
    ]
    emails = an.get_emails_from_people_resources(resources)

    assert emails == [email1, email2]


def test_get_emails_given_emails_json():
    email1 = fake.email()
    email2 = fake.email()
    emails_json = [{"address": email1}, {"address": email2}]

    assert an.get_emails_given_emails_json(emails_json) == [email1, email2]


def test_get_person_from_people_given_email():
    email = fake.email()
    id = fake.uuid4()
    people = [
        {
            "email_addresses": [{"address": email}],
            "identifiers": ["action_network:" + id],
        },
    ]
    assert an.get_person_id_from_people_given_email(email, people) == id


def test_get_person_by_email(mocked_responses, member_email, member_person_response):
    href = f"{an.AN_API_URL}/people?filter=email_address eq '{member_email}'"
    mocked_responses.add(
        responses.GET,
        href,
        json=member_person_response,
    )
    person_response = requests.get(href).json()
    assert person_response == member_person_response


def test_get_membership_status_member(
    member_taggings_response,
):
    assert an.get_membership_status_from_taggings(member_taggings_response)


def test_get_membership_status_nonmember(
    nonmember_taggings_response,
):
    assert an.get_membership_status_from_taggings(nonmember_taggings_response) is False


def test_get_id_from_href():
    id = fake.uuid4()
    href = fake.url() + id
    assert an.get_id_from_href(href) == id


def test_get_tag_href_from_tagging():
    href = fake.url()
    tagging = {"_links": {"osdi:tag": {"href": href}}}
    assert an.get_tag_href_from_tagging(tagging) == href


def test_membership_no_tags(nonmember_taggings_response):
    assert an.get_membership_status_from_taggings(nonmember_taggings_response) is False


def test_membership_tags(member_taggings_response):
    assert an.get_membership_status_from_taggings(member_taggings_response)
