from django.apps import AppConfig
from django.conf import settings

from actionnetwork.email import create


def create_email(sender, **kwargs):
    newspage = kwargs["instance"]
    response = create(
        newspage.title,
        newspage.body,
        "STL DSA",
        "info@stldsa.org",
        settings.ACTIONNETWORK_API_KEYS["main"],
    )
    print(response.content)


class NewsConfig(AppConfig):
    name = "news"

    def ready(self):
        import news.signals
