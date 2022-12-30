from news.models import NewsPage
from events.models import Event


def test_save_main_event(db):
    event = Event()
    update = NewsPage(main_event=event)
    assert update.main_event == event
