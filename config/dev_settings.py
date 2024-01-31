"""Django Settings"""

import environ

env = environ.Env()


DEBUG = True

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path("stldsa")
BASE_DIR = ROOT_DIR

WAGTAIL_SITE_NAME = "St Louis DSA"
TIME_ZONE = "America/Chicago"
SITE_ID = 1
WAGTAIL_I18N_ENABLED = False
USE_I18N = False
USE_TZ = True
LANGUAGE_CODE = "en"
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
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "rest_framework.authtoken",
    "home",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.styleguide",
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
    "storages",
    "django_sass",
    "django_extensions",
    "anymail",
]

LOCAL_APPS = [
    "stldsa.users",
    "events",
    "committees",
    "news",
    "about",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIGRATION_MODULES = {"sites": "stldsa.contrib.sites.migrations"}
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
        "NAME": "django.contrib.auth.password_validation."
        + "UserAttributeSimilarityValidator"
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
    "allauth.account.middleware.AccountMiddleware",
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
MEDIA_URL = "media/"

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
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "stldsa.utils.context_processors.settings_context",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = "STL DSA <noreply@stldsa.org>"
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = "[STL DSA]"

# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = "dj-admin"

# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "stldsa.users.adapters.MyAccountAdapter"
SOCIALACCOUNT_ADAPTER = "stldsa.users.adapters.SocialAccountAdapter"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_FORMS = {"signup": "stldsa.users.forms.SignUpForm"}
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
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

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
SECRET_KEY = env("DJANGO_SECRET_KEY")

LOCAL_SERVE_MEDIA_FILES = True
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

ALLOWED_HOSTS = ["*"]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

WAGTAILADMIN_BASE_URL = "https://localhost:8000"
CACHE_URL = None

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "werkzeug": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
