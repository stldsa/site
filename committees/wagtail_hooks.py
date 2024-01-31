from wagtail import hooks

from committees.views import formation_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return formation_viewset
