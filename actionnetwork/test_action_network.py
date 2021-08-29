import action_network as an
from faker import Faker

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


def test_get_id_from_href():
    id = fake.uuid4()
    href = fake.url() + id
    assert an.get_id_from_href(href) == id


def test_get_tag_href_from_tagging():
    href = fake.url()
    tagging = {"_links": {"osdi:tag": {"href": href}}}
    assert an.get_tag_href_from_tagging(tagging) == href
