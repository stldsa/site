import dj_database_url
from config.settings_base import env, TEMPLATES, INSTALLED_APPS


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
INSTALLED_APPS = INSTALLED_APPS + ["anymail"]  # noqa F405
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"


ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN"),
    "MAILGUN_API_URL": env("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
}


# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
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
