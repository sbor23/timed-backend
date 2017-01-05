"""
Django settings for timed project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import configparser
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'timed/config.ini'))

ldap_config    = config['ldap']
github_config  = config['github']
redmine_config = config['redmine']


def trueish(value):
    """Cast a string to a boolean."""
    return value.lower() in ('true', '1', 'yes')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jpfx&3nyjat!)g1vbp7n=#6cgeu*vnwyymxehm-%jc+482%^ej'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crispy_forms',
    'timed_api',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'timed.middleware.DisableCSRFMiddleware',
]

ROOT_URLCONF = 'timed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'timed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'timed',
        'USER':     'timed',
        'PASSWORD': 'timed',
        'HOST':     'localhost'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = False
USE_L10N = False

DATETIME_FORMAT = 'd.m.Y H:i:s'
DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i:s'

DECIMAL_SEPARATOR = '.'

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'PAGINATE_BY': None,
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_METADATA_CLASS':
        'rest_framework_json_api.metadata.JSONAPIMetadata',
    'EXCEPTION_HANDLER':
        'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=60),
    'JWT_ALLOW_REFRESH': True,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

JSON_API_FORMAT_KEYS = 'dasherize'
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = True

APPEND_SLASH = False

GITHUB_API_URL   = github_config.get('GITHUB_API_URL')
GITHUB_ISSUE_URL = github_config.get('GITHUB_ISSUE_URL')

REDMINE_API_URL             = redmine_config.get('REDMINE_API_URL')
REDMINE_ISSUE_URL           = redmine_config.get('REDMINE_ISSUE_URL')
REDMINE_BASIC_AUTH          = trueish(redmine_config.get('REDMINE_BASIC_AUTH'))
REDMINE_BASIC_AUTH_USER     = redmine_config.get('REDMINE_BASIC_AUTH_USER')
REDMINE_BASIC_AUTH_PASSWORD = redmine_config.get('REDMINE_BASIC_AUTH_PASSWORD')

AUTH_LDAP_ALWAYS_UPDATE_USER = True

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name':  'sn',
    'email':      'mail'
}

AUTH_LDAP_SERVER_URI       = ldap_config.get('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN          = ldap_config.get('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD    = ldap_config.get('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_USER_DN_TEMPLATE = ldap_config.get('AUTH_LDAP_USER_DN_TEMPLATE')
