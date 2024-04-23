"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import os
import pathlib
# from core import config 
from core.settings.base import *
from core.utils.secret_key import generate_secret_key_if_missing
import environ
env = environ.Env()
environ.Env.read_env()

email = env('EMAIL', default='default_value')

passw = env('PASSWORD', default='default_value')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = generate_secret_key_if_missing(BASE_DATA_DIR)

DJANGO_DB = get_env('DJANGO_DB', DJANGO_DB_SQLITE)
DATABASES = {'default': DATABASES_ALL[DJANGO_DB]}

MIDDLEWARE.append('organizations.middleware.DummyGetSessionMiddleware')
MIDDLEWARE.append('core.middleware.UpdateLastActivityMiddleware')
if INACTIVITY_SESSION_TIMEOUT_ENABLED:
    MIDDLEWARE.append('core.middleware.InactivitySessionTimeoutMiddleWare')

ADD_DEFAULT_ML_BACKENDS = False

LOGGING['root']['level'] = get_env('LOG_LEVEL', 'WARNING')

DEBUG = get_bool_env('DEBUG', False)

DEBUG_PROPAGATE_EXCEPTIONS = get_bool_env('DEBUG_PROPAGATE_EXCEPTIONS', False)

SESSION_COOKIE_SECURE = get_bool_env('SESSION_COOKIE_SECURE', False)

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

RQ_QUEUES = {}

SENTRY_DSN = get_env(
    'SENTRY_DSN',
    'https://68b045ab408a4d32a910d339be8591a4@o227124.ingest.sentry.io/5820521'
)
SENTRY_ENVIRONMENT = get_env('SENTRY_ENVIRONMENT', 'opensource')

FRONTEND_SENTRY_DSN = get_env(
    'FRONTEND_SENTRY_DSN',
    'https://5f51920ff82a4675a495870244869c6b@o227124.ingest.sentry.io/5838868')
FRONTEND_SENTRY_ENVIRONMENT = get_env('FRONTEND_SENTRY_ENVIRONMENT', 'opensource')

EDITOR_KEYMAP = json.dumps(get_env("EDITOR_KEYMAP"))

# email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'data@indikaai.com'
EMAIL_HOST_PASSWORD = 'cvgm jqly ytmg ilnb'
# EMAIL_BACKEND = 'django_ses.SESBackend'

# # Your AWS region where you set up SES (e.g., us-west-2)
# AWS_SES_REGION_NAME = 'ap-south-1'

# # Your AWS region's endpoint for SES
# AWS_SES_REGION_ENDPOINT = 'email-smtp.ap-south-1.amazonaws.com'

# # Your AWS Access Key
# AWS_ACCESS_KEY_ID = ''

# # Your AWS Secret Key
# AWS_SECRET_ACCESS_KEY = ''



from data_studio import __version__
from data_studio.core.utils import sentry
sentry.init_sentry(release_name='data-studio', release_version=__version__)

# we should do it after sentry init
from data_studio.core.utils.common import collect_versions
versions = collect_versions()

# in Data Studio Community version, feature flags are always ON
FEATURE_FLAGS_DEFAULT_VALUE = True
# or if file is not set, default is using offline mode
FEATURE_FLAGS_OFFLINE = get_bool_env('FEATURE_FLAGS_OFFLINE', True)

from core.utils.io import find_file
FEATURE_FLAGS_FILE = get_env('FEATURE_FLAGS_FILE', 'feature_flags.json')
FEATURE_FLAGS_FROM_FILE = True
try:
    from core.utils.io import find_node
    find_node('data_studio', FEATURE_FLAGS_FILE, 'file')
except IOError:
    FEATURE_FLAGS_FROM_FILE = False

STORAGE_PERSISTENCE = get_bool_env('STORAGE_PERSISTENCE', True)
