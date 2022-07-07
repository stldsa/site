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
    email.schedule(
        f"{newspage.action_network_href}/schedule",
        kwargs["go_live_at"],
        settings.ACTIONNETWORK_API_KEYS["main"],
    )


@receiver(page_published, sender=NewsPage)
def create_email(sender, **kwargs):
    newspage = kwargs["instance"]
    revision = newspage.save_revision()
    # main_story_html = (
    #     f"<h1>{newspage.main_story_heading}</h1><div>{newspage.main_story_copy}</div>"
    # )

    # def related_story_html(story):
    #     return f'<div class="row"><div class="col-sm-4 my-auto"><img src="https://bucketeer-addd2217-1ffa-41ff-b050-fd915562796e.s3.amazonaws.com/bucketeer-addd2217-1ffa-41ff-b050-fd915562796e/media/public/images/{story["image"]}"></div><div class="col"><h2>{story["heading"]}</h2><p>{story["copy"]}</p></div></div>'

    # related_stories_html = [
    #     related_story_html(block.value) for block in newspage.related_stories
    # ]
    response = email.create(
        newspage.title,
        # main_story_html + "".join(related_stories_html),
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
