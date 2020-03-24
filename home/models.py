from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

class HomePage(Page):
    template = 'pages/home.html'
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("banner_title")
    ]
