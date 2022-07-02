from django.conf import settings
from news.signals import page_publish_scheduled
from actionnetwork.email import create, schedule
from django.dispatch import receiver
from django.db.models.signals import post_save
from news.models import NewsPage
from django.utils import timezone
from wagtail.models import PageRevision
from wagtail.signals import page_published


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
    schedule(
        f"{newspage.action_network_href}/schedule",
        kwargs["go_live_at"],
        settings.ACTIONNETWORK_API_KEYS["main"],
    )


@receiver(page_published, sender=NewsPage)
def create_email(sender, **kwargs):
    newspage = kwargs["instance"]
    data = create(
        newspage.title,
        newspage.body,
        "STL DSA",
        "info@stldsa.org",
        settings.ACTIONNETWORK_API_KEYS["main"],
    )
    action_network_href = data.json()["_links"]["self"]["href"]
    newspage.action_network_href = action_network_href
    newspage.save()
    # status = "calculating"
    # while status != "draft":re
    #     time.sleep(1)
    #     response = requests.get(
    #         response["_links"]["self"]["href"],
    #         headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
    #     )
    #     data = json.loads(response.content)
    #     status = data["status"]
    # schedule_helper = data["_links"]["osdi:schedule_helper"]["href"]
    # response = requests.post(
    #     schedule_helper,
    #     headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
    #     json={"scheduled_start_date": datetime.datetime(2024, 1, 1)},
    # )
    # print(response.contents)
