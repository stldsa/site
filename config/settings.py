# mysite/settings.py
from configurations import Configuration, values
from decouple import config
import boto3

import os
import json
import environ
import secrets
import dj_database_url

env = environ.Env()


class Base(Configuration):
    ACTIONNETWORK_API_KEYS = values.DictValue({"main": ""}, environ_prefix=None)
    # stl_dsa/config/settings.py - 2 = stl_dsa/
    ROOT_DIR = environ.Path(__file__) - 2
    APPS_DIR = ROOT_DIR.path("stl_dsa")
    BASE_DIR = ROOT_DIR
    if READ_DOT_ENV_FILE := env.bool("DJANGO_READ_DOT_ENV_FILE", default=False):
        env.read_env(str(ROOT_DIR.path(".env")))
    DEBUG = values.BooleanValue(True)

    WAGTAIL_SITE_NAME = "St Louis DSA"
    # SITE_ID = {"domain": "https://stldsa.org", "name": "St Louis DSA"}
    TIME_ZONE = "America/Chicago"
    SITE_ID = 1
    WAGTAIL_I18N_ENABLED = True
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
        ("en", "English"),
        ("es", "Spanish"),
        ("bs", "Bosnian"),
    ]
    ROOT_URLCONF = "config.urls"
    WSGI_APPLICATION = "config.wsgi.application"
    DJANGO_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.admin",
        "django.forms",
    ]
    THIRD_PARTY_APPS = [
        "phonenumber_field",
        "crispy_forms",
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "rest_framework",
        "rest_framework.authtoken",
        "home",  # home app before wagtail.admin overrides admin template
        # "search",
        "wagtail_localize",
        "wagtail_localize.locales",
        "wagtail.contrib.forms",
        "wagtail.contrib.redirects",
        "wagtail.contrib.modeladmin",
        "wagtail.embeds",
        "wagtail.sites",
        "wagtail.users",
        "wagtail.snippets",
        "wagtail.documents",
        "wagtail.images",
        "wagtail.search",
        "wagtail.admin",
        "wagtail",
        "modelcluster",
        "taggit",
        "wagtailfontawesome",
        "wagtailmenus",
        "storages",
    ]

    LOCAL_APPS = [
        "stl_dsa.users",
        "events",
        "committees",
        "news",
    ]
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    MIGRATION_MODULES = {"sites": "stl_dsa.contrib.sites.migrations"}
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    ]
    AUTH_USER_MODEL = "users.User"
    LOGIN_REDIRECT_URL = "users:detail"
    LOGIN_URL = "account_login"

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    ]
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.common.BrokenLinkEmailsMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    ]

    # STATIC
    STATIC_ROOT = str(BASE_DIR.path("staticfiles"))
    STATIC_URL = "/staticfiles/"
    STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    ]

    # MEDIA
    # ------------------------------------------------------------------------------
    MEDIA_ROOT = str(BASE_DIR.path("media"))
    MEDIA_URL = "/media/"

    # TEMPLATES
    # ------------------------------------------------------------------------------
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [str(APPS_DIR.path("templates"))],
            "OPTIONS": {
                "loaders": [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ],
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                    "stl_dsa.utils.context_processors.settings_context",
                    "wagtail.contrib.settings.context_processors.settings",
                    "wagtailmenus.context_processors.wagtailmenus",
                ],
            },
        }
    ]

    FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
    CRISPY_TEMPLATE_PACK = "bootstrap4"

    # FIXTURES
    # ------------------------------------------------------------------------------
    FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

    # SECURITY
    # ------------------------------------------------------------------------------
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"

    # EMAIL
    # ------------------------------------------------------------------------------
    EMAIL_BACKEND = env(
        "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
    )
    EMAIL_TIMEOUT = 5

    # ADMIN
    # ------------------------------------------------------------------------------
    ADMIN_URL = values.Value("admin")

    # LOGGING
    # ------------------------------------------------------------------------------
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }

    # django-allauth
    # ------------------------------------------------------------------------------
    ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
    ACCOUNT_AUTHENTICATION_METHOD = "email"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_ADAPTER = "stl_dsa.users.adapters.MyAccountAdapter"
    SOCIALACCOUNT_ADAPTER = "stl_dsa.users.adapters.SocialAccountAdapter"
    ACCOUNT_SESSION_REMEMBER = True
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_FORMS = {"signup": "stl_dsa.users.forms.SignUpForm"}
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
    ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

    # DRF
    # -------------------------------------------------------------------------------
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.TokenAuthentication",
        ),
        "DEFAULT_PERMISSION_CLASSES": (
            "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        ),
    }

    ACTIONNETWORK_API_KEYS = json.loads(
        os.environ.get("ACTIONNETWORK_API_KEYS", '{"main": "1234567890abcdefg"}')
    )  # The default key is not real
    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
    SECRET_KEY = env("DJANGO_SECRET_KEY", default=secrets.token_urlsafe())


class Dev(Base):
    DEBUG = True
    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
    DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///stl_dsa")}
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }
    EMAIL_BACKEND = env(
        "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
    )
    INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + Base.INSTALLED_APPS
    INSTALLED_APPS = INSTALLED_APPS + [
        "debug_toolbar",
        "django_extensions",
    ]
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    MIDDLEWARE = Base.MIDDLEWARE + [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    NOTEBOOK_ARGUMENTS = [
        "--ip",
        "0.0.0.0",
        "--port",
        "8888",
        "--allow-root",
        "--no-browser",
    ]
    LOCAL_SERVE_MEDIA_FILES = True
    WAGTAILADMIN_BASE_URL = "http://localhost:8000"


class Local(Dev):
    DATABASES = values.DatabaseURLValue("postgres:///stl_dsa")


class Docker(Dev):
    DATABASES = values.DatabaseURLValue("postgres://postgres:postgres@db:5432/postgres")


class Test(Dev):

    TEST_RUNNER = "django.test.runner.DiscoverRunner"
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    TEMPLATES = Base.TEMPLATES
    TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        )
    ]
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


class Production(Base):
    DEBUG = False
    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
    # CACHES = values.CacheURLValue("redis://127.0.0.1:6379/1")

    # SECURITY
    # ------------------------------------------------------------------------------
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
    )
    SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
    SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
        "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
    )

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    TEMPLATES = Base.TEMPLATES
    TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        )
    ]

    DEFAULT_FROM_EMAIL = env(
        "DJANGO_DEFAULT_FROM_EMAIL", default="STL DSA <noreply@stldsa.org>"
    )
    SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
    EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[STL DSA]")

    # Anymail (Mailgun)
    # ------------------------------------------------------------------------------
    INSTALLED_APPS = Base.INSTALLED_APPS + ["anymail"]  # noqa F405
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    @property
    def ANYMAIL(self):
        return {
            "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
            "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN"),
            "MAILGUN_API_URL": env(
                "MAILGUN_API_URL", default="https://api.mailgun.net/v3"
            ),
        }

    # LOGGING
    # ------------------------------------------------------------------------------
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
        },
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.security.DisallowedHost": {
                "level": "ERROR",
                "handlers": ["console", "mail_admins"],
                "propagate": True,
            },
        },
    }

    DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}

    LOCAL_SERVE_MEDIA_FILES = False

    PUBLIC_MEDIA_DEFAULT_ACL = "public-read"
    PUBLIC_MEDIA_LOCATION = "media/public"

    AWS_ACCESS_KEY_ID = env("BUCKETEER_AWS_ACCESS_KEY_ID", default=None)
    AWS_SECRET_ACCESS_KEY = env("BUCKETEER_AWS_SECRET_ACCESS_KEY", default=None)
    AWS_STORAGE_BUCKET_NAME = env("BUCKETEER_BUCKET_NAME", default=None)
    S3_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
    AWS_S3_REGION_NAME = env("BUCKETEER_AWS_REGION", default=None)
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_SIGNATURE_VERSION = env("S3_SIGNATURE_VERSION", default="s3v4")
    AWS_S3_ENDPOINT_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400", "ACL": "public-read"}

    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "stl_dsa.utils.storage_backends.PublicMediaStorage"

    PRIVATE_MEDIA_DEFAULT_ACL = "private"
    PRIVATE_MEDIA_LOCATION = "media/private"
    PRIVATE_FILE_STORAGE = "stl_dsa.utils.storage_backends.PrivateMediaStorage"

    WAGTAILDOCS_SERVE_METHOD = "direct"
    WAGTAILADMIN_BASE_URL = "https://stldsa.org"

    MIDDLEWARE_CLASSES = "raygun4py.middleware.django.Provider"
    RAYGUN4PY_API_KEY = "ocPGkwhkAFhhkFnvyGCNOg"


class Staging(Production):
    WAGTAILADMIN_BASE_URL = "https://stldsa-staging.herokuapp.com"
