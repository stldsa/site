import datetime
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.search import index
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BlockQuoteBlock, CharBlock
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from events.models import Event


class NewsIndexPage(Page):
    message = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("message", classname="full")]
    subpage_types = [
        "news.NewsPage",  # appname.ModelName
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
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
        ("related_story", {"heading": event.title, "paragraph": event.description})
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
    main_story_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    main_story_heading = models.CharField(max_length=500, null=True, blank=True)
    main_story_copy = RichTextField(blank=True)
    action_network_href = models.URLField(blank=True, null=True)
    related_stories = StreamField(
        [
            (
                "related_story",
                blocks.StructBlock(
                    [
                        ("heading", blocks.CharBlock()),
                        ("copy", blocks.TextBlock()),
                        ("image", ImageChooserBlock()),
                    ],
                ),
            )
        ],
        null=True,
        blank=True,
        collapsed=False,
        default=upcoming_events_as_related_stories,
        use_json_field=True,
    )

    parent_page_type = ["news.NewsIndexPage"]  # appname.ModelName
    search_fields = Page.search_fields + [
        index.SearchField("main_story_copy"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("main_story_image"),
        FieldPanel("main_story_heading"),
        FieldPanel("main_story_copy", classname="full"),
        FieldPanel("related_stories"),
    ]


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
                        ("image", ImageChooserBlock()),
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
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date_published"),
        FieldPanel("body"),
    ]
