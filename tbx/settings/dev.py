from .base import *  # noqa

DEBUG = True

SECURE_SSL_REDIRECT = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGEME!!!'

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

BASE_URL = 'http://localhost:8000'

# URL to direct preview requests to
PREVIEW_URL = 'http://localhost:8001/preview'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PASSWORD_VALIDATORS = []


MEDIA_PREFIX = BASE_URL

try:
    from .local import *  # noqa
except ImportError:
    pass
