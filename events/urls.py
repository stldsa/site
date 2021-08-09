from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventsView.as_view(), name="events"),
]
