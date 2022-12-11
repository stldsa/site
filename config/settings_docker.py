from config.settings_dev import *

import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://postgres:postgres@localhost:5432/postgres"
    )
}
