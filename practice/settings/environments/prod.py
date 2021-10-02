"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""

from practice.settings.components.base import *

DEBUG = env("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = ["*"]

STATIC_ROOT = BASE_DIR.joinpath("..", "staticfiles")

INTERNAL_IPS = [
    '127.0.0.1',
]
