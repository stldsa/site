from django.db import models
from datetime import datetime
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from events.models import Event
from news.models import NewsPage
from wagtail.fields import RichTextField


class HomePage(Page):
    highlighted_campaign = models.CharField(max_length=100, blank=False, null=True)
    highlighted_description = RichTextField(blank=False, null=True)
    action_network_embed_api_endpoint = models.URLField(blank=True, null=True)
    call_to_action = models.URLField(blank=True, null=True)

    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("highlighted_campaign"),
        FieldPanel("highlighted_description"),
        FieldPanel("call_to_action"),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context["events"] = (
            Event.objects.filter(start__gte=datetime.now().date())
            .exclude(title__icontains="members only")
            .order_by("start")[:4]
        )
        context["update"] = NewsPage.objects.live().latest("last_published_at")
        return context
