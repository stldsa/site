import datetime
from typing import Any, List
from django import forms
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.search import index
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BlockQuoteBlock, CharBlock
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from events.models import Event


class NewsIndexPage(Page):
    message = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("message", classname="full")]
    subpage_types = [
        "news.NewsPage",
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        updates = self.get_children().live().order_by("-last_published_at")
        paginator = Paginator(updates, 5)
        page = request.GET.get("page")
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        context["updates"] = resources
        return context

    class Meta:
        verbose_name = "Updates"


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


class NewsPageRelatedStory(Orderable):
    page = ParentalKey(
        "news.NewsPage", on_delete=models.CASCADE, related_name="stories"
    )
    description = RichTextField(null=True, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    related_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="related_event",
    )

    panels = [FieldPanel("description"), FieldPanel("related_event")]


class NewsPage(Page):
    """A Wagtail Page for our weekly newsletter"""

    description = RichTextField(blank=True)
    action_network_href = models.URLField(blank=True, null=True)
    parent_page_types = ["news.NewsIndexPage"]
    subpage_types: List[Any] = []
    search_fields = Page.search_fields + [
        index.SearchField("description"),
    ]

    title_widget = forms.TextInput()
    content_panels = [
        FieldPanel(
            "title",
            heading="Subject",
            widget=title_widget,
            help_text=("Email subject line / page title."),
        ),
        InlinePanel("stories", heading="Stories", label="Story"),
    ]

    class Meta:
        verbose_name = "Update"


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
