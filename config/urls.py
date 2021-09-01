from stl_dsa.users.views import UserSignupView, UserLoginView
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_framework.authtoken.views import obtain_auth_token
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from events.api import urls as events_api_urls

# from sphinxdoc import urls as sphinxdoc_urls


urlpatterns = (
    [
        # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
        path(
            "about/",
            TemplateView.as_view(template_name="pages/about.html"),
            name="about",
        ),
        # Django Admin, use {% url 'admin:index' %}
        path(settings.ADMIN_URL, admin.site.urls),
        path("myDSA/", include("stl_dsa.users.urls", namespace="users")),
        path("signup/", UserSignupView.as_view(), name="account_signup"),
        path("login/", UserLoginView.as_view(), name="account_login"),
        path("", include("allauth.urls")),
        path("events/", include("events.urls")),
        path(
            "fullcalendar/",
            TemplateView.as_view(template_name="fullcalendar.html"),
            name="fullcalendar",
        ),
        path("api/", include(events_api_urls)),
        path("auth-token/", obtain_auth_token),
        # re_path(r"^docs/", include(sphinxdoc_urls)),
        path("cms/", include(wagtailadmin_urls)),
        path("documents/", include(wagtaildocs_urls)),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + i18n_patterns(
        # path("search/", search_views.search, name="search"),
        path("", include(wagtail_urls)),
    )
)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
