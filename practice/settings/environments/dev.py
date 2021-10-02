"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""

from practice.settings.components.base import *

DEBUG = env("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = ["*"]

STATIC_ROOT = BASE_DIR.joinpath("..", "staticfiles")

INSTALLED_APPS += [
    "debug_toolbar",
]

INTERNAL_IPS = [
    '127.0.0.1',
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}
