import os
import sys
import logging
from logging.config import dictConfig
from django.contrib.messages import constants as messages
from django.core.management.utils import get_random_secret_key
from environs import Env

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# CONSTANTS
DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["*"])
LOGLEVEL = env.log_level("LOG_LEVEL", "INFO")
SECRET_KEY = env.str("SECRET_KEY", "wewqer$//§((83742387&&§_?/DFash")

# Application definition
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_tables2",
    "django_filters",
    "extra_views",
    "crispy_forms",
    "newshows",
    "django_q",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "new_shows.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "new_shows.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'P4S',
        'USER': 'admin',
        'PASSWORD': 'Busc0pan1',
        'HOST': '192.168.42.167',
        'PORT': '32769',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "assets")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


CRISPY_TEMPLATE_PACK = "bootstrap4"
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Configuration for DjangoQ
Q_CLUSTER = {
    "name": "DjangORM", #use Django ORM as backend 
    "workers": 1, #max 1 parallel tasks
    #'timeout': 90, # disable timeout
    "retry": 180000,  # set the retry so high, that long running tasks are not rescheduled
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
    "catch_up": False,  # do not run old unrun schedules
    #"sync": True, #Don't run asynchronously
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # Formatters ###########################################################
    'formatters': {
      'console': {
          'format': '%(name)-12s %(levelname)-8s %(message)s'
      },
      'file': {
          'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
      },
    },
    # Handlers #############################################################
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'main.log',
            'formatter': 'file'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'p4s': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'p4s.log',
            'formatter': 'file'
        },
    },
    # Loggers ####################################################################
    'loggers': {
        'django': {
            'handlers': ['file',],
            'level': 'DEBUG',
        },
        'root': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        'p4s': {
            'handlers': ['p4s', 'console'],
            'level': 'DEBUG',
        },
    },
}