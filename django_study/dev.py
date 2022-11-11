from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_study',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'pgdb',
        'PORT': 5432,
        'TIMEZONE': 'UTC'
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@redisdb:6379/0",
        # redis://:password@bundlev2redis:6379/1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@redisdb:6379/1",
        # redis://:password@bundlev2redis:6379/1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}