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


# class NewsPageForm(WagtailAdminPageForm):
#     def save(self, commit=True):
#         page = super().save(commit=False)
#         # created_datetime = page.save_revision().created_at
# upcoming_events = Event.objects.filter(
#     date__range=(created_datetime, created_datetime + datetime.timedelta(days=7))
# )
#         # Update the duration field from the submitted dates
#         page.related_stories = [
#             (
#                 "related_story",
#                 [
#                     ("heading", "TestHeading"),
#                     ("paragraph", "this is a test p"),
#                     ("image", None),
#                 ],
#             )
#         ]

#         if commit:
#             page.save()
#         return page


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
    main_story_image = models.ImageField(null=True)
    main_story_header = models.CharField(max_length=500, null=True, blank=True)
    main_story_copy = RichTextField(blank=True)
    action_network_href = models.URLField(blank=True, null=True)
    related_stories = StreamField(
        [
            (
                "related_story",
                blocks.StructBlock(
                    [
                        ("heading", blocks.CharBlock(form_classname="full title")),
                        ("paragraph", blocks.TextBlock()),
                        ("image", ImageChooserBlock()),
                    ],
                ),
            )
        ],
        null=True,
        blank=True,
        collapsed=False,
        # default=[
        #     ("related_story", {"heading": "1", "paragraph": "this is p1"}),
        #     ("related_story", {"heading": "2", "paragraph": "this is p1"}),
        # ],
        default=upcoming_events_as_related_stories,
        use_json_field=True,
    )

    parent_page_type = ["news.NewsIndexPage"]  # appname.ModelName
    search_fields = Page.search_fields + [
        index.SearchField("main_story_copy"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("main_story_header"),
        FieldPanel("main_story_copy", classname="full"),
        FieldPanel("related_stories"),
    ]

    # base_form_class = NewsPageForm


# class RelatedStory(models.Model):
#     title = models.CharField(max_length=255, null=True)
#     link_external = models.URLField("External link", null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     image = models.ImageField(null=True, blank=True)

#     panels = [
#         FieldPanel("title"),
#         FieldPanel("link_external"),
#         FieldPanel("description"),
#         FieldPanel("image"),
#     ]

#     class Meta:
#         abstract = True


# class NewsPageRelatedStories(Orderable, RelatedStory):
#     news_page = ParentalKey(
#         NewsPage, on_delete=models.CASCADE, related_name="related_stories"
#     )


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
