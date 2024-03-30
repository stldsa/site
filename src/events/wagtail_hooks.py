from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from events.models import Event


class EventViewSet(SnippetViewSet):
    model = Event
    base_url_path = "events"
    list_display = ("title", "start")
    icon = "date"
    list_per_page = 15

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(title__contains="Tech Committee Drop In Hours")


register_snippet(EventViewSet)
