from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from news.models import NewsPage


class UpdatesViewSet(SnippetViewSet):
    model = NewsPage
    menu_label = "Updates"
    icon = "mail"
    base_url_path = "updates"
    list_display = ("__str__", "first_published_at")
    ordering = ("-first_published_at",)
    list_filter = ("has_unpublished_changes", "live")
    list_per_page = 10


register_snippet(UpdatesViewSet)


@hooks.register("construct_explorer_page_queryset")
def order_updates_reverse_chron(parent_page, pages, request):
    if parent_page.slug == "updates":
        pages = pages.order_by("-first_published_at")

    return pages
