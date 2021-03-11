from events.api import views
from django.urls import path

urlpatterns = [path("events/", views.list, name="events_api")]
