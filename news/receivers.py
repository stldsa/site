from django.conf import settings
from news.signals import page_publish_scheduled
from actionnetwork import email
from django.dispatch import receiver
from django.db.models.signals import pre_save
from news.models import NewsPage
from django.utils import timezone
from wagtail.models import PageRevision
from wagtail.signals import page_published
from render_block import render_block_to_string
import polling2 as polling
import requests


# @receiver(pre_save, sender=PageRevision)
# def send_page_publish_scheduled(sender, **kwargs):
#     revision = kwargs["instance"]
#     print("pre-instantiation")
#     page = revision.as_page_object()
#     print("post-instantiation")
#     if page.specific_class == NewsPage:
#         print("news page!!!")
#         print(page.action_network_href)
#         if page.action_network_href:
#             email.edit(
#                 page.action_network_href,
#                 {
#                     "subject": page.title,
#                     "body": render_block_to_string(
#                         "news/news_page.html", "content", context={"page": page}
#                     ),
#                     "from": "STL DSA",
#                     "reply_to": "info@stldsa.org",
#                 },
#                 settings.ACTIONNETWORK_API_KEYS["main"],
#             )
#             print("email edited!!!")
#         else:
#             print("Pre-Create")
#             response = email.create(
#                 page.title,
#                 # main_story_html + "".join(related_stories_html),
#                 render_block_to_string(
#                     "news/news_page.html", "content", context={"page": page}
#                 ),
#                 "STL DSA",
#                 "info@stldsa.org",
#                 settings.ACTIONNETWORK_API_KEYS["main"],
#             )
#             print("post_create")
#             action_network_href = response.json()["_links"]["self"]["href"]
#             print(action_network_href)
#             # page.action_network_href = action_network_href


@receiver(page_published, sender=NewsPage)
def schedule_send(sender, **kwargs):
    print("publish receiver called")
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
    print("publish receiver finished")
