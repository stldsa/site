from django.urls import path

from . import views

urlpatterns = [
    path('', views.CommitteeList.as_view(), name='committees'),

]