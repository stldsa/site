from wagtail import hooks


@hooks.register("construct_main_menu")
def hide_pages(request, menu_items):
    menu_items[:] = [
        item
        for item in menu_items
        if item.name not in ["explorer", "documents", "images", "reports"]
    ]
