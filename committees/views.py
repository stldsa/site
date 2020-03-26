from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from committees.models import Committee

class CommitteeList(ListView):
    model = Committee
    context_object_name = 'committee_list'