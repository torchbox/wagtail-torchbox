from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost']
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8111'


INSTALLED_APPS += (
    'wagtail.contrib.wagtailstyleguide',
)

# Facebook JSSDK app Id
FB_APP_ID = '323944607389'


try:
    from .local import *
except ImportError:
    pass

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

try:
    from .local import *
except ImportError:
    pass

