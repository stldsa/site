from wagtail import hooks
from django.utils.html import format_html
from django.templatetags.static import static


@hooks.register("construct_main_menu")
def hide_pages(request, menu_items):
    menu_items[:] = [
        item
        for item in menu_items
        if item.name not in ["explorer", "documents", "images", "reports"]
    ]


@hooks.register("construct_homepage_summary_items")
def hide_homepage_summary_items(request, items):
    items.clear()


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/wagtail.css"))
