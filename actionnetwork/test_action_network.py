import action_network as an
import pytest
from faker import Faker

fake = Faker()


@pytest.mark.vcr()
def test_get_events():
    an.get_events()


# @pytest.mark.vcr()
# def test_get_tags_from_email():
#     email = fake.email()
#     tag_list = an.get_taggings(email)

#     assert "Voting Member" in tag_list
