# -*- coding: utf-8 -*-
"""
Django settings for stormcrew project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OPENSHIFT_GEAR_NAME = os.environ.get('OPENSHIFT_GEAR_NAME', None)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SERVER = True
DEBUG = False

# ########## DEBUG CONFIGURATION
# if os.environ.get("DEBUG_DJANGO", None):
#     # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
#     DEBUG = True
# else:
#     DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = "hdgMLmH/Qc24uzmLBpwspiIGGB9GyEnomjaE0gwwAWE="
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    join(BASE_DIR, 'fixtures'),
)
if DEBUG:
    FIXTURE_DIRS = FIXTURE_DIRS + (join(BASE_DIR, 'local_fixtures'), )
########## END FIXTURE CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Ivan Kobzev', 'Ivan.Kobzev@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION

########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/Los_Angeles'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'ru-RU'

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    join(BASE_DIR, 'locale'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# if OPENSHIFT_GEAR_NAME:
#     MEDIA_ROOT = join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')
# else:
#     MEDIA_ROOT = join(BASE_DIR, 'media')

MEDIA_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'media').replace('\\', '/')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION

########## MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'static').replace('\\', '/')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    join(BASE_DIR, 'static'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'south', # Database migration helpers:
    'crispy_forms', # Form layouts
    'social_auth', # registration
    'sorl.thumbnail', # image thumbnails
    'postman_custom',
    'postman',
    'tastypie',
    'provider',
    'provider.oauth2'
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'users', # custom users app
    'trip',
    'utils',
    'geo',
    'party_api.aviasales',
    'blog'
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

########## END APP CONFIGURATION


########## URL Configuration
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'
########## End URL Configuration

########## django-secure
SECURE = False
if SECURE:
    INSTALLED_APPS += ("djangosecure", )

    # set this to 60 seconds and then to 518400 when you can prove it works
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_FRAME_DENY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_SSL_REDIRECT = True
########## end django-secure


########## AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    'social_auth.backends.facebook.FacebookBackend',
)
NO_AVATAR_IMG = STATIC_URL + 'img/no-avatar.jpg'
########## END AUTHENTICATION CONFIGURATION

########## SOCIAL AUTH CONFIGURATION
FACEBOOK_APP_ID = '205781592952444'
FACEBOOK_API_SECRET = '6995e3fd3d2517a722d105b1282a5bcc'
FACEBOOK_SKIP_POST_ON_WALL = os.environ.get('FACEBOOK_SKIP_POST_ON_WALL', False)

FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'user_birthday', 'publish_stream']
FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}

# TODO
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/users/cabinet/"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/users/cabinet/"
LOGOUT_REDIRECT_URL = "/"
# TODO provide select of login source here (fb/vk/tw etc.)
LOGIN_URL = "/accounts/login/facebook/"

# TODO
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'users.pipeline.store_additional_fields',
    'social_auth.backends.pipeline.user.update_user_details'
)

########## END SOCIAL AUTH CONFIGURATION

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
########## END AUTHENTICATION CONFIGURATION

########## TRAVELPAYOUTS
TRAVELPAYOUTS_TOKEN = os.environ.get('TRAVELPAYOUTS_TOKEN', '')
TRAVELPAYOUTS_MARKER = os.environ.get('TRAVELPAYOUTS_MARKER', '')

########## END TRAVELPAYOUTS

########## Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
########## END Custom user app defaults


########## SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
########## END SLUGLIFIER

########## POSTMAN
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_DISALLOW_ANONYMOUS = True
########## END POSTMAN

LOCAL = os.environ.get("DJANGO_LOCAL", False)

################## PRODUCTION SETTINGS

if DEBUG and not OPENSHIFT_GEAR_NAME:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    email_folder = os.path.join(os.path.dirname(BASE_DIR), 'debug/emails')
    if not os.path.exists(email_folder):
        os.makedirs(email_folder)
    EMAIL_FILE_PATH = email_folder
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025

    # MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    # INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    FILL_TEST_DATA = True
    CACHE_BOOTSTRAP = True
else:
    TEMPLATE_DEBUG = DEBUG

    ########## SITE CONFIGURATION
    # Hosts/domain names that are valid for this site
    # See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    ########## END SITE CONFIGURATION

    ########## CACHING
    # from memcacheify import memcacheify
    # CACHES = memcacheify()
    ########## END CACHING
    FILL_TEST_DATA = False
    CACHE_BOOTSTRAP = False

if os.environ.get('EMAIL_HOST', None):
    ########## EMAIL
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.com')
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')
    EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
    EMAIL_USE_TLS = False
    if os.environ.get('EMAIL_USE_TLS', False):
        EMAIL_USE_TLS = True
    SERVER_EMAIL = EMAIL_HOST_USER
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    ########## END EMAIL

######### GEOIP
if OPENSHIFT_GEAR_NAME:
    GEOIP_PATH = join(os.environ.get('OPENSHIFT_DATA_DIR'), 'geoip')
elif LOCAL:
    GEOIP_PATH = None
else:
    GEOIP_PATH = '/usr/share/GeoIP'
######### END GEOIP


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social_auth.context_processors.social_auth_by_name_backends',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'utils.context_processors.custom_settings',
    'postman.context_processors.inbox',
    # Your stuff: custom template context processers go here
)


# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    join(BASE_DIR, 'templates'),
)

if DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
else:
    # TEMPLATE_LOADERS = (
    #     #('django.template.loaders.cached.Loader', (
    #     ((
    #         'django.template.loaders.filesystem.Loader',
    #         'django.template.loaders.app_directories.Loader',
    #     )),
    # )
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

# See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'
########## END TEMPLATE CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_local_true': {
            '()': 'config.log.RequireLocalTrue'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'rotate_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../log/main.log'),
            'when': 'midnight',
            'interval': 1, # day
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
        'db_rotate_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../log/db.log'),
            'when': 'midnight',
            'interval': 1, # day
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
            'filters': ['require_local_true'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'api_aviasales_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../log/api_aviasales.log'),
            'when': 'midnight',
            'interval': 1, # day
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'api_aviasales': {
            'handlers': ['api_aviasales_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'requests.packages.urllib3': {
            'handlers': ['api_aviasales_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['rotate_file'],
            'level': 'DEBUG',
        }
    }
}
if DEBUG and os.environ.get("DJANGO_LOG_DB", None):
    LOGGING['loggers']['django.db'] = {
        'level': 'DEBUG',
        'handlers': ['console', 'db_rotate_file'],
        'propagate': False,
    }
if DEBUG:
    LOGGING['loggers']['']['handlers'].append('console')
########## END LOGGING CONFIGURATION


########## Your stuff: Below this line define 3rd party libary settings

try:
    from local_settings import *
except ImportError:
    SERVER = True

if SERVER:
    from server_settings import *

    RAVEN_CONFIG = {
        'dsn': 'http://352e7c1857cf4f11b7dbe71dd4891d93:a3abffeff7f74e4684822dbe241738b1@188.226.156.5/2',
    }

    INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
    )