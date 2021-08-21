import action_network
import validators
import pytest


@pytest.mark.vcr()
@pytest.mark.parametrize("resource", ["events", "tags"])
def test_get_resource(resource):
    assert action_network.get_resource(resource, "main").status_code == 200


@pytest.mark.vcr()
def test_get_events():
    action_network.get_events()


@pytest.mark.vcr()
def test_get_tags():
    assert action_network.get_tags().status_code == 200


@pytest.mark.vcr()
def test_get_voting_member_tag_taggings_href():
    assert validators.url(action_network.get_tag_taggings_href("Voting Members"))
