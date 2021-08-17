import action_network
import vcr


@vcr.use_cassette()
def test_get_events():
    action_network.get_events()