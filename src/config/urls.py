from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.views import obtain_auth_token
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from events.api import urls as events_api_urls
from stldsa.users.views import UserSignupView
from actionnetwork import views


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("events/", include("events.urls")),
    path("myDSA/", include("stldsa.users.urls", namespace="users")),
    path(
        "signup/",
        UserSignupView.as_view(),
        name="account_signup",
    ),
    path(
        "login/",
        LoginView.as_view(template_name="account/login.html"),
        name="account_login",
    ),
    path("", include("allauth.urls")),
    path(
        "person-helper/",
        views.person_helper,
        name="person-helper",
    ),
    path("api/", include(events_api_urls)),
    path("auth-token/", obtain_auth_token),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.LOCAL_SERVE_MEDIA_FILES:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
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
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
