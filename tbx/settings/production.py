from .base import *

DEBUG = False


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': 'wagtail-torchbox'
    }
}


INSTALLED_APPS += (
    'djcelery',
    'kombu.transport.django',
    'gunicorn',

    'wagtail.contrib.wagtailfrontendcache',
)


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'KEY_PREFIX': 'torchbox',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}


COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]


SERVER_EMAIL = "root@by-web-2.torchbox.com"


# CELERY SETTINGS
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://'
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_LOG_COLOR = False


# Facebook JSSDK app Id
FB_APP_ID = '323944607389'


try:
    from .local import *
except ImportError:
    pass
