from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from events.models import Event


class EventAdmin(ModelAdmin):
    model = Event
    base_url_path = "events"
    list_display = ("title",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(title__contains="Tech Committee Drop In Hours")


modeladmin_register(EventAdmin)
