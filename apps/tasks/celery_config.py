from kombu import Exchange, Queue

# timezone
CELERY_TIMEZONE = 'UTC'

default_exchange = Exchange('default', type='direct')

CELERY_IMPORTS = ("apps.tasks.async_tasks", )

CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default', max_priority=10),
)
CELERYD_CONCURRENCY = 2 # celery worker number

# create broker if not exists
CELERY_CREATE_MISSING_QUEUES = True

CELERYD_MAX_TASKS_PER_CHILD = 100  # max tasks number per celery worker

CELERYD_FORCE_EXECV = True  # avoid deadlock

CELERY_ACKS_LATE = True

CELERYD_PREFETCH_MULTIPLIER = 4

# speed limit
CELERY_DISABLE_RATE_LIMITS = True
CELERY_TASK_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ["json", "pickle"]

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'