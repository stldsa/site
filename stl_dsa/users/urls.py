from django.urls import path

from stl_dsa.users.views import UserDetailView, UserUpdateView

app_name = "users"
urlpatterns = [
    path("", view=UserDetailView, name="detail"),
    path("update/", view=UserUpdateView, name="update"),
]
