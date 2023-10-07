"""Django Settings"""
import secrets
import environ

env = environ.Env()


DEBUG = env.bool("DJANGO_DEBUG", default=True)

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path("stl_dsa")
BASE_DIR = ROOT_DIR
if READ_DOT_ENV_FILE := env.bool("DJANGO_READ_DOT_ENV_FILE", default=True):
    env.read_env(str(ROOT_DIR.path(".env")))

WAGTAIL_SITE_NAME = "St Louis DSA"
TIME_ZONE = "America/Chicago"
SITE_ID = 1
WAGTAIL_I18N_ENABLED = False
USE_I18N = False
USE_TZ = True
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
    "stl_dsa.users",
    "events",
    "committees",
    "news",
    "about",
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
                "stl_dsa.utils.context_processors.settings_context",
                "wagtail.contrib.settings.context_processors.settings",
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
X_FRAME_OPTIONS = env("DJANGO_X_FRAME_OPTIONS", default="DENY")
SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT", default=False)

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_TIMEOUT = 5
MAILGUN_API_KEY = env("MAILGUN_API_KEY", default=None)
MAILGUN_DOMAIN = env("MAILGUN_DOMAIN", default=None)
MAILGUN_PUBLIC_KEY = env("MAILGUN_PUBLIC_KEY", default=None)
MAILGUN_SMTP_LOGIN = env("MAILGUN_SMTP_LOGIN", default=None)
MAILGUN_SMTP_PASSWORD = env("MAILGUN_SMTP_PASSWORD", default=None)
MAILGUN_SMTP_PORT = env("MAILGUN_SMTP_PORT", default=None)
MAILGUN_SMTP_SERVER = env("MAILGUN_SMTP_SERVER", default=None)
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="STL DSA <noreply@stldsa.org>"
)
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[STL DSA]")

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)


ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY", default=""),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN", default=""),
    "MAILGUN_API_URL": env("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
}


# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL", default="dj-admin/")

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
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", default=True)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "stl_dsa.users.adapters.MyAccountAdapter"
SOCIALACCOUNT_ADAPTER = "stl_dsa.users.adapters.SocialAccountAdapter"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_FORMS = {"signup": "stl_dsa.users.forms.SignUpForm"}
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

ACTIONNETWORK_API_KEYS = env.dict("ACTIONNETWORK_API_KEYS")
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
SECRET_KEY = env("DJANGO_SECRET_KEY", default=secrets.token_urlsafe())

LOCAL_SERVE_MEDIA_FILES = True
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": env("AWS_STORAGE_BUCKET_NAME", default=None),
            "access_key": env("AWS_ACCESS_KEY_ID", default=None),
            "secret_key": env("AWS_SECRET_ACCESS_KEY", default=None),
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "0.0.0.0", "127.0.0.1"])

DATABASES = {
    "default": env.db(default="postgres://postgres:postgres@localhost:5432/postgres")
}

WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL", default="https://localhost:8000")
CACHE_URL = env("CACHE_URL", default=None)

# Remove after upgrade to Django 5.0
FORM_RENDERER = "django.forms.renderers.DjangoDivFormRenderer"
