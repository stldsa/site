from wagtail.admin.viewsets.model import ModelViewSet
from committees.models import Formation


class FormationViewSet(ModelViewSet):
    model = Formation

    form_fields = ["name"]


formation_viewset = FormationViewSet(
    "formation"
)  # defines /admin/person/ as the base URL
