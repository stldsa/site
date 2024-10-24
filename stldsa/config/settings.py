"""Django Settings"""

import os

import environ

env = environ.Env()


DEBUG = env.bool("DJANGO_DEBUG")

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
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = env("DJANGO_X_FRAME_OPTIONS")
SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT")

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = os.getenv("DJANGO_EMAIL_BACKEND")
EMAIL_TIMEOUT = 5
MAILGUN_PUBLIC_KEY = os.getenv("MAILGUN_PUBLIC_KEY")
MAILGUN_SMTP_LOGIN = os.getenv("MAILGUN_SMTP_LOGIN")
MAILGUN_SMTP_PASSWORD = os.getenv("MAILGUN_SMTP_PASSWORD")
MAILGUN_SMTP_PORT = os.getenv("MAILGUN_SMTP_PORT")
MAILGUN_SMTP_SERVER = os.getenv("MAILGUN_SMTP_SERVER")
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX")

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND")


ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.getenv("MAILGUN_DOMAIN"),
    "MAILGUN_API_URL": os.getenv("MAILGUN_API_URL"),
}


# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL")

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
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION")
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

ACTIONNETWORK_API_KEYS = {
    "main": os.getenv("AN_CHAPTER_KEY"),
    "comms": os.getenv("AN_COMMS_KEY"),
    "community": os.getenv("AN_COMMUNITY_KEY"),
    "sns": os.getenv("AN_SNS_KEY"),
    "electoral": os.getenv("AN_ELECTORAL_KEY"),
    "tech": os.getenv("AN_TECH_KEY"),
    "transit": os.getenv("AN_TRANSIT_KEY"),
    "housing": os.getenv("AN_HOUSING_KEY"),
    "northcounty": os.getenv("AN_NORTH_COUNTY_KEY"),
    "afrosoc": os.getenv("AN_AFROSOC_KEY"),
    "gnd": os.getenv("AN_GND_KEY"),
    "labor": os.getenv("AN_LABOR_KEY"),
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
SECRET_KEY = env("DJANGO_SECRET_KEY")

LOCAL_SERVE_MEDIA_FILES = True
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME"),
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {"default": env.db()}

WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL")
CACHE_URL = env("CACHE_URL")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
