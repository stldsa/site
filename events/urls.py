from django.urls import path

from events import views

urlpatterns = [
    path("", views.EventsView.as_view(), name="events"),
    path("<int:id>/", views.EventDetailView.as_view(), name="event-detail"),
]
