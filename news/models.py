from django.db import models
from wagtail.search import index
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail_blocks.blocks import HeaderBlock


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
        context["blogpages"] = blogpages
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
        StreamFieldPanel("additional_content"),
    ]


class DocumentPage(Page):
    date_published = models.DateField("Last Updated", blank=True, null=True)
    body = StreamField([
        ('section', blocks.StreamBlock([
            ('header', HeaderBlock()),
            ('text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('subsection', blocks.StreamBlock([
                ('header', HeaderBlock()),
                ('text', blocks.TextBlock()),
                ('subsubsection', blocks.StreamBlock([
                    ('header', HeaderBlock()),
                    ('text', blocks.TextBlock()),
                ]))
            ]))
        ]))
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date_published"),
        StreamFieldPanel("body")
    ]
