from django.conf import settings
from news.signals import page_publish_scheduled
from actionnetwork import email
from django.dispatch import receiver
from django.db.models.signals import post_save
from news.models import NewsPage
from django.utils import timezone
from wagtail.models import PageRevision
from wagtail.signals import page_published
from render_block import render_block_to_string
import json


@receiver(post_save, sender=PageRevision)
def send_page_publish_scheduled(sender, **kwargs):
    revision = kwargs["instance"]
    go_live_at = revision.approved_go_live_at
    if go_live_at and go_live_at > timezone.now():
        page = revision.as_page_object()
        page_publish_scheduled.send(
            sender=page.specific_class,
            instance=page.specific,
            revision=revision,
            go_live_at=go_live_at,
        )


@receiver(page_publish_scheduled, sender=NewsPage)
def schedule_send(sender, **kwargs):
    newspage = kwargs["instance"]
    print(newspage.id)
    print(newspage.action_network_href)
    url = newspage.action_network_href
    email.schedule(
        f"{url}/schedule",
        kwargs["go_live_at"],
        settings.ACTIONNETWORK_API_KEYS["main"],
    )


@receiver(page_published, sender=NewsPage)
def create_email(sender, **kwargs):
    newspage = kwargs["instance"]
    response = email.create(
        newspage.title,
        render_block_to_string(
            "news/news_page.html", "content", context={"page": newspage}
        ),
        "STL DSA",
        "info@stldsa.org",
        settings.ACTIONNETWORK_API_KEYS["main"],
    )
    action_network_href = response["_links"]["self"]["href"]
    newspage.action_network_href = action_network_href
    newspage.save()
