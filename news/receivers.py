from django.conf import settings
from news.signals import page_publish_scheduled
from actionnetwork import email
from django.dispatch import receiver
from django.db.models.signals import pre_save
from news.models import NewsletterPage
from django.utils import timezone
from wagtail.signals import page_published
import polling2 as polling
import requests


@receiver(page_published, sender=NewsletterPage)
def schedule_send(sender, **kwargs):
    newspage = kwargs["instance"]
    revision = kwargs["revision"]
    go_live_at = revision.approved_go_live_at
    if go_live_at and go_live_at > timezone.now():
        polling.poll(
            lambda: requests.get(newspage.action_network_href).json()["total_targeted"]
            > 0,
            step=1,
            timeout=10,
            step_function=lambda step: step + 2,
        )
        email.schedule(
            f"{newspage.action_network_href}/schedule",
            revision.approved_go_live_at,
            settings.ACTIONNETWORK_API_KEYS["main"],
        )
