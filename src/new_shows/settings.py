import os
import sys
import logging.config
from django.contrib.messages import constants as messages
from django.core.management.utils import get_random_secret_key
from environs import Env

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# CONSTANTS
DEBUG = env.bool('DEBUG', True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['*'])
LOGLEVEL = env.log_level("LOG_LEVEL", "INFO")
SECRET_KEY = env.str("SECRET_KEY", "wewqer$//§((83742387&&§_?/DFash")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'django_filters',
    'extra_views',
    'crispy_forms',
    'newshows',
    'background_task',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'new_shows.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'new_shows.wsgi.application'


DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env("SQL_USER", "user"),
        "PASSWORD": env("SQL_PASSWORD", "password"),
        "HOST": env("SQL_HOST", "localhost"),
        "PORT": env("SQL_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'assets')

STATIC_URL = '/static/'
STATIC_ROOT = [os.path.join(BASE_DIR, 'staticfiles'),]


CRISPY_TEMPLATE_PACK = 'bootstrap4'
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

# Logging Configuration
LOGGING_CONFIG = None

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

logging.config.dictConfig({
    'version': 1,

    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', ],
        },
    },
})
