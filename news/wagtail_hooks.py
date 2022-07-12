from wagtail import hooks


@hooks.register("construct_explorer_page_queryset")
def show_my_profile_only(parent_page, pages, request):
    # If we're in the 'user-profiles' section, only show the user's own profile
    if parent_page.slug == "updates":
        pages = pages.order_by("-first_published_at")

    return pages
