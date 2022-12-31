from news.models import NewsPage
from events.models import Event


def test_save_related_event(db):
    event = Event()
    update = NewsPage(related_event=event)
    assert update.related_event == event
