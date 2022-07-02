from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from modelcluster.fields import ParentalKey
from wagtail.search import index
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import BlockQuoteBlock, CharBlock
from wagtail.admin.panels import FieldPanel, InlinePanel
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
        page = request.GET.get("page")
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        context["blogpages"] = resources
        return context


class NewsPage(Page):
    heading = models.CharField(max_length=500, null=True, blank=True)
    body = RichTextField(blank=True)
    action_network_href = models.URLField(blank=True, null=True)

    parent_page_type = ["news.NewsIndexPage"]  # appname.ModelName
    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("body", classname="full"),
        InlinePanel("related_stories", label="Related Stories"),
    ]


class RelatedStory(models.Model):
    title = models.CharField(max_length=255, null=True)
    link_external = models.URLField("External link", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("link_external"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    class Meta:
        abstract = True


class NewsPageRelatedStories(Orderable, RelatedStory):
    news_page = ParentalKey(
        NewsPage, on_delete=models.CASCADE, related_name="related_stories"
    )


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
