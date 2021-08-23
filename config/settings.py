# mysite/settings.py

from configurations import Configuration, values

import os
import json
import environ
import secrets

env = environ.Env()


class Base(Configuration):
    ACTIONNETWORK_API_KEYS = values.DictValue({"main": ""}, environ_prefix=None)
    # stl_dsa/config/settings.py - 2 = stl_dsa/
    ROOT_DIR = environ.Path(__file__) - 2
    APPS_DIR = ROOT_DIR.path("stl_dsa")

    READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
    if READ_DOT_ENV_FILE:
        # OS environment variables take precedence over variables from .env
        env.read_env(str(ROOT_DIR.path(".env")))

    # GENERAL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(True)
    # Local time zone. Choices are
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # though not all of them may be available with every OS.
    # In Windows, this must be set to your system time zone.
    TIME_ZONE = "America/Chicago"
    # https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = "en-us"
    # https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1
    # https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
    LOCALE_PATHS = [ROOT_DIR.path("locale")]

    # URLS
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
    ROOT_URLCONF = "config.urls"
    # https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = "config.wsgi.application"

    # APPS
    # ------------------------------------------------------------------------------
    DJANGO_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # "django.contrib.humanize", # Handy template tags
        "django.contrib.admin",
        "django.forms",
    ]
    THIRD_PARTY_APPS = [
        "crispy_forms",
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "rest_framework",
        "rest_framework.authtoken",
        "home",  # home app before wagtail.admin overrides admin template
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
        "wagtail.contrib.search_promotions",
        "wagtail.admin",
        "wagtail.core",
        "taggit",
        "modelcluster",
        "wagtailfontawesome",
        "wagtail_blocks",
    ]

    LOCAL_APPS = [
        "stl_dsa.users.apps.UsersConfig",
        # Your stuff: custom apps go here
        "events",
        "committees",
        "phonenumber_field",
        "news",
        "django_seed",
    ]
    # https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    # MIGRATIONS
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
    MIGRATION_MODULES = {"sites": "stl_dsa.contrib.sites.migrations"}

    # AUTHENTICATION
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    ]
    # https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
    AUTH_USER_MODEL = "users.User"
    # https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
    LOGIN_REDIRECT_URL = "users:redirect"
    # https://docs.djangoproject.com/en/dev/ref/settings/#login-url
    LOGIN_URL = "account_login"

    # PASSWORDS
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
    PASSWORD_HASHERS = [
        # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    ]
    # https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # MIDDLEWARE
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#middleware
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
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = str(ROOT_DIR("staticfiles"))
    # https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = "/static/"
    # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
    # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    ]

    # MEDIA
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = str(APPS_DIR("media"))
    # https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = "/media/"

    # TEMPLATES
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#templates
    TEMPLATES = [
        {
            # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
            "DIRS": [str(APPS_DIR.path("templates"))],
            "OPTIONS": {
                # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
                # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
                "loaders": [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ],
                # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                    "stl_dsa.utils.context_processors.settings_context",
                ],
            },
        }
    ]

    # https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
    FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

    # http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
    CRISPY_TEMPLATE_PACK = "bootstrap4"

    # FIXTURES
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
    FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

    # SECURITY
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
    SESSION_COOKIE_HTTPONLY = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
    CSRF_COOKIE_HTTPONLY = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
    SECURE_BROWSER_XSS_FILTER = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
    X_FRAME_OPTIONS = "DENY"

    # EMAIL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = env(
        "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
    )
    # https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
    EMAIL_TIMEOUT = 5

    # ADMIN
    # ------------------------------------------------------------------------------
    # Django Admin URL.
    ADMIN_URL = "admin/"
    # https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = [("""Tyler Schlichenmeyer""", "tyler.schlichenmeyer@gmail.com")]
    # https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS

    # LOGGING
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # See https://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
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
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_AUTHENTICATION_METHOD = "email"
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_ADAPTER = "stl_dsa.users.adapters.MyAccountAdapter"
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    SOCIALACCOUNT_ADAPTER = "stl_dsa.users.adapters.SocialAccountAdapter"
    ACCOUNT_SESSION_REMEMBER = True
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_FORMS = {"signup": "stl_dsa.users.forms.SignUpForm"}
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    # django-reset-framework
    # -------------------------------------------------------------------------------
    # django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.TokenAuthentication",
        ),
        "DEFAULT_PERMISSION_CLASSES": (
            "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        ),
    }
    # Your stuff...
    # ------------------------------------------------------------------------------
    WAGTAIL_SITE_NAME = "St Louis DSA"
    ACTIONNETWORK_API_KEYS = json.loads(os.environ.get("ACTIONNETWORK_API_KEYS", "{}"))
    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
    SECRET_KEY = env("DJANGO_SECRET_KEY", default=secrets.token_urlsafe())


class Docker(Base):
    DATABASES = values.DatabaseURLValue("postgres://postgres:postgres@db:5432/postgres")

    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

    # CACHES
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    # EMAIL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = env(
        "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
    )

    # WhiteNoise
    # ------------------------------------------------------------------------------
    # http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
    INSTALLED_APPS = [
        "whitenoise.runserver_nostatic"
    ] + Base.INSTALLED_APPS  # noqa F405

    # django-debug-toolbar
    # ------------------------------------------------------------------------------
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE = Base.MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

    # django-extensions
    # ------------------------------------------------------------------------------
    # https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
    INSTALLED_APPS += ["django_extensions"]  # noqa F405

    # Your stuff...
    # ------------------------------------------------------------------------------
    HAYSTACK_CONNECTIONS = {
        "default": {
            "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
        },
    }


class Local(Base):
    # GENERAL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

    # DATABASES
    # ------------------------------------------------------------------------------
    DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///stl_dsa")}

    # CACHES
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    # EMAIL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = env(
        "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
    )

    # WhiteNoise
    # ------------------------------------------------------------------------------
    # http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
    INSTALLED_APPS = [
        "whitenoise.runserver_nostatic"
    ] + Base.INSTALLED_APPS  # noqa F405

    # django-debug-toolbar
    # ------------------------------------------------------------------------------
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    # MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

    # django-extensions
    # ------------------------------------------------------------------------------
    # https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
    INSTALLED_APPS += ["django_extensions"]  # noqa F405

    # Your stuff...
    # ------------------------------------------------------------------------------
    HAYSTACK_CONNECTIONS = {
        "default": {
            "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
        },
    }


class Test(Base):
    # GENERAL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
    TEST_RUNNER = "django.test.runner.DiscoverRunner"

    # CACHES
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    # PASSWORDS
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

    # TEMPLATES
    # ------------------------------------------------------------------------------
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

    # EMAIL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


class Production(Base):
    # https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["stldsa.org"])

    # CACHES
    # ------------------------------------------------------------------------------
    CACHES = values.CacheURLValue("redis://127.0.0.1:6379/1")

    # SECURITY
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
    SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
    # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
    SESSION_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
    CSRF_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
    # TODO: set this to 60 seconds first and then to 518400 once you prove the former works
    SECURE_HSTS_SECONDS = 60
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
    )
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
    SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
    # https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
    SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
        "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
    )

    # STATIC
    # ------------------------
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    # MEDIA
    # ------------------------------------------------------------------------------

    # TEMPLATES
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#templates
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

    # EMAIL
    # ------------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
    DEFAULT_FROM_EMAIL = env(
        "DJANGO_DEFAULT_FROM_EMAIL", default="STL DSA <noreply@stldsa.org>"
    )
    # https://docs.djangoproject.com/en/dev/ref/settings/#server-email
    SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
    # https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
    EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[STL DSA]")

    # ADMIN
    # ------------------------------------------------------------------------------
    # Django Admin URL regex.
    ADMIN_URL = values.Value("admin")

    # Anymail (Mailgun)
    # ------------------------------------------------------------------------------
    # https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
    INSTALLED_APPS = Base.INSTALLED_APPS + ["anymail"]  # noqa F405
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    # https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
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
    # https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # See https://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
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

    HAYSTACK_CONNECTIONS = {
        "default": {
            "ENGINE": "haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine",
            "URL": "https://stldsa.org",
            "INDEX_NAME": "haystack",
        },
    }
