from django.db import models
from datetime import datetime
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from action_network import get_events
from events.models import Event
from news.models import NewsPage


class HomePage(Page):
    template = "pages/home.html"
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    body = RichTextField(blank=True)
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("body", classname="full"),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context["events"] = Event.objects.filter(
            date__gte=datetime.today().date()
        ).order_by("date")[:4]
        context["update"] = NewsPage.objects.all().order_by("-date")[0]
        return context
