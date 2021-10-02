from datetime import timedelta

CELERY_TASK_RESULT_EXPIRES = 3600

CELERY_BEAT_SCHEDULE = {
    "message_send": {
        "task": "",
    },

}
