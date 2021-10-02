from practice.settings import env
from practice.settings.components.base import TIME_ZONE
USER_AGENTS_CACHE = "default"

# REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_URL = env("REDIS_URL", default='django-db')
AMQP_URL = env("AMQP_URL", default='amqp://admin:admin@0.0.0.0:5672/')

DB_URL = REDIS_URL
BROKER_URL = AMQP_URL
CELERY_result_backend = DB_URL
CELERY_BROKER_URL = BROKER_URL

CELERY_TASK_TRACK_STARTED = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TIME_LIMIT = 60 * 60
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}
