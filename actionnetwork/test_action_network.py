import action_network as an
import json
import responses
from os import environ
from faker import Faker
from unittest.mock import patch, Mock
from config.settings import ACTIONNETWORK_API_KEYS

fake = Faker()


# def test_events_resource():
#     events = an.Resource("events", "main").list
#     assert len(events) > 1


# def test_person_resource():
#     id = fake.uuid4()
#     an.Resource("people", group="main", id=id)


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

@patch('action_network.requests.get')
def test_get_person_by_email(mock_get):
    email = fake.email()
    id = fake.uuid4()
    an_apikey = "fakekey"
    an.get_person_by_email(email)
    mock_get.assert_called_once_with(
        f'https://actionnetwork.org/api/v2/people?filter=email_address eq \'{email}\'',
        headers={"OSDI-API-Token": an_apikey}
    )

@responses.activate
def test_get_membership_status():
    email = fake.email()
    test_member_person = {
        '_embedded': {
            'osdi:taggings': [
                {
                    '_links': {
                        'osdi:tag': {
                            'href': 'https://actionnetwork.org/api/v2/tags/7cb02320-3ecc-4479-898e-67769a1bf7be'
                        }
                    }
                }
            ]
        }
    }
    responses.add(responses.GET,
            f'https://actionnetwork.org/api/v2/people?filter=email_address eq \'{email}\'',
            json={'_embedded': { 'osdi:people': [ test_member_person ]}}
            )

    assert an.get_membership_status(email) is True
    

@responses.activate
def test_get_membership_status_nonmember():
    email = fake.email()
    test_nonmember_person = {
        '_embedded': {
            'osdi:taggings': [
                {
                    '_links': {
                        'osdi:tag': {
                            'href': 'https://actionnetwork.org/api/v2/tags/random-tag-id'
                        }
                    }
                }
            ]
        }
    }
    responses.add(responses.GET,
        f'https://actionnetwork.org/api/v2/people?filter=email_address eq \'{email}\'',
        json={'_embedded': { 'osdi:people': [ test_nonmember_person ]}}
    )
    assert an.get_membership_status(email) is False


def test_get_id_from_href():
    id = fake.uuid4()
    href = fake.url() + id
    assert an.get_id_from_href(href) == id


def test_get_tag_href_from_tagging():
    href = fake.url()
    tagging = {"_links": {"osdi:tag": {"href": href}}}
    assert an.get_tag_href_from_tagging(tagging) == href
