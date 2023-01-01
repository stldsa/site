from wagtail import hooks


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
