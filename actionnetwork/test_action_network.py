import action_network as an
import pytest
from faker import Faker

fake = Faker()


@pytest.mark.vcr()
def test_get_events():
    an.get_events()
