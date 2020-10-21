from .base import *  # noqa

DEBUG = True

SECURE_SSL_REDIRECT = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGEME!!!'

# Enable FE component library
PATTERN_LIBRARY_ENABLED = True

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

BASE_URL = 'http://localhost:8000'

# URL to direct preview requests to
PREVIEW_URL = 'http://localhost:8001/preview'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PASSWORD_VALIDATORS = []

# Enable Wagtail's style guide in Wagtail's settings menu.
# http://docs.wagtail.io/en/stable/contributing/styleguide.html
INSTALLED_APPS += ["wagtail.contrib.styleguide"]  # noqa

# Set URL for the preview iframe. Should point at Gatsby.
PREVIEW_URL = 'http://localhost:8003/preview/'

MEDIA_PREFIX = BASE_URL

CORS_ORIGIN_ALLOW_ALL = True

try:
    from .local import *  # noqa
except ImportError:
    pass
