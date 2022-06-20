from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.search import index
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BlockQuoteBlock, CharBlock
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock


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
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        context["blogpages"] = resources
        return context


class NewsPage(Page):
    date = models.DateField("Post date")
    body = RichTextField(blank=True)

    parent_page_type = ["news.NewsIndexPage"]  # appname.ModelName
    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body", classname="full"),
    ]


class InfoPage(Page):
    body = RichTextField(blank=True)
    additional_content = StreamField(
        [("embed", blocks.RawHTMLBlock())], null=True, blank=True
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
    )

    content_panels = Page.content_panels + [
        FieldPanel("date_published"),
        FieldPanel("body"),
    ]
