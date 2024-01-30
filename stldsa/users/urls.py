from django.urls import path

from stldsa.users.views import UserDetailView, UserUpdateView

app_name = "users"
urlpatterns = [
    path("", view=UserDetailView.as_view(), name="detail"),
    path("update/", view=UserUpdateView.as_view(), name="update"),
]
