import pytest


@pytest.mark.firefox_arguments("-headless")
def test_full_calendar(selenium, live_server):
    selenium.get(live_server + "/fullcalendar")
