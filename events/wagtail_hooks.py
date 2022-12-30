from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from events.models import Event


class EventAdmin(ModelAdmin):
    model = Event
    base_url_path = "events"
    list_display = ("title",)


modeladmin_register(EventAdmin)
