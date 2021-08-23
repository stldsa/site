import action_network
import pytest


@pytest.mark.vcr()
def test_get_events():
    action_network.get_events()
