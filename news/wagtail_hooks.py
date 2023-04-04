from wagtail import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from news.models import NewsPage


class UpdatesAdmin(ModelAdmin):
    model = NewsPage
    menu_label = "Updates"
    menu_icon = "mail"
    base_url_path = "updates"
    list_display = ("__str__", "first_published_at")
    ordering = ("-first_published_at",)
    list_filter = ("has_unpublished_changes", "live")
    list_per_page = 10


modeladmin_register(UpdatesAdmin)


@hooks.register("construct_explorer_page_queryset")
def order_updates_reverse_chron(parent_page, pages, request):
    if parent_page.slug == "updates":
        pages = pages.order_by("-first_published_at")

    return pages
