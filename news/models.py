import datetime
from django import forms
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from wagtail.search import index
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BlockQuoteBlock, CharBlock, RichTextBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from events.models import Event
from actionnetwork import email
from render_block import render_block_to_string
from django.utils import timezone
import polling2 as polling
import requests


class NewsIndexPage(Page):
    message = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("message", classname="full")]
    subpage_types = [
        "news.NewsPage",  # appname.ModelName
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-last_published_at")
        paginator = Paginator(blogpages, 5)
        page = request.GET.get("page")
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        context["blogpages"] = resources
        return context


def upcoming_events_as_related_stories():
    return [
        (
            "related_story",
            {"heading": event.title, "copy": event.description},
        )
        for event in list(
            Event.objects.filter(
                start__range=(
                    datetime.datetime.now(),
                    datetime.datetime.now() + datetime.timedelta(days=7),
                )
            )
        )
    ]


class NewsPage(Page):
    """A Wagtail Page for our weekly newsletter"""

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    main_copy = RichTextField(blank=True)
    action_network_href = models.URLField(blank=True, null=True)
    stories = StreamField(
        [("related_story", RichTextBlock())],
        null=True,
        blank=True,
        collapsed=False,
        use_json_field=True,
    )

    parent_page_type = ["news.NewsIndexPage"]  # appname.ModelName
    search_fields = Page.search_fields + [
        index.SearchField("main_copy"),
    ]

    title_widget = forms.TextInput()
    content_panels = [
        FieldPanel(
            "title",
            heading="Subject",
            widget=title_widget,
        ),
        MultiFieldPanel(
            (
                FieldPanel("banner_image"),
                FieldPanel("main_copy"),
            ),
            "Main Story",
        ),
        FieldPanel("stories", heading="Other Stories"),
    ]

    def save(self, *args, **kwargs):
        if self.action_network_href:
            email.edit(
                self.action_network_href,
                {
                    "subject": self.title,
                    "body": render_block_to_string(
                        "news/news_page.html", "content", context={"page": self}
                    ),
                    "from": "STL DSA",
                    "reply_to": "info@stldsa.org",
                },
                settings.ACTIONNETWORK_API_KEYS["main"],
            )
        else:
            response = email.create(
                self.title,
                # main_story_html + "".join(related_stories_html),
                render_block_to_string(
                    "news/news_page.html", "content", context={"page": self}
                ),
                "STL DSA",
                "info@stldsa.org",
                settings.ACTIONNETWORK_API_KEYS["main"],
            )
            links = response.json().get("_links")
            if links:
                action_network_href = links["self"]["href"]
            else:
                action_network_href = None
            self.action_network_href = action_network_href

        if self.go_live_at and self.go_live_at > timezone.now():
            polling.poll(
                lambda: requests.get(
                    self.action_network_href,
                    headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
                )
                .json()
                .get("total_targeted", 0)
                > 0,
                step=1,
                timeout=10,
                step_function=lambda step: step + 2,
            )
            email.schedule(
                f"{self.action_network_href}/schedule",
                self.go_live_at,
                settings.ACTIONNETWORK_API_KEYS["main"],
            )
        super().save(*args, **kwargs)  # Call the "real" save() method.


class InfoPage(Page):
    body = RichTextField(blank=True)
    additional_content = StreamField(
        [("embed", blocks.RawHTMLBlock())],
        null=True,
        blank=True,
        use_json_field=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        FieldPanel("additional_content"),
    ]


class DocumentPage(Page):
    date_published = models.DateField("Last Updated", blank=True, null=True)
    body = StreamField(
        [
            (
                "section",
                blocks.StreamBlock(
                    [
                        ("header", CharBlock()),
                        ("text", blocks.RichTextBlock()),
                        ("quote", BlockQuoteBlock()),
                        (
                            "subsection",
                            blocks.StreamBlock(
                                [
                                    ("header", CharBlock()),
                                    ("text", blocks.TextBlock()),
                                    (
                                        "subsubsection",
                                        blocks.StreamBlock(
                                            [
                                                ("header", CharBlock()),
                                                ("text", blocks.TextBlock()),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            )
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date_published"),
        FieldPanel("body"),
    ]
