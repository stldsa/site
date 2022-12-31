from wagtail.admin.viewsets.model import ModelViewSet
from news.models import NewsPage


class UpdateViewSet(ModelViewSet):
    model = NewsPage
    icon = "mail"
    form_fields = ["title", "description"]


update_viewset = UpdateViewSet("update", url_prefix="updates")
