from .base import *  # noqa

DEBUG = True

SECURE_SSL_REDIRECT = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGEME!!!"

# Enable FE component library
PATTERN_LIBRARY_ENABLED = True

INTERNAL_IPS = ("127.0.0.1", "10.0.2.2")

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# URL to direct preview requests to
PREVIEW_URL = "http://localhost:8001/preview"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = ["*"]

AUTH_PASSWORD_VALIDATORS = []

# Enable Wagtail's style guide in Wagtail's settings menu.
# http://docs.wagtail.io/en/stable/contributing/styleguide.html
INSTALLED_APPS += ["wagtail.contrib.styleguide"]  # noqa

# Set URL for the preview iframe. Should point at Gatsby.
PREVIEW_URL = "http://localhost:8003/preview/"

MEDIA_PREFIX = WAGTAILADMIN_BASE_URL

# Adds Django Debug Toolbar
INSTALLED_APPS.append("debug_toolbar")  # noqa
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa

# Override in `local.py`
SHOW_TOOLBAR = True

DEBUG_TOOLBAR_CONFIG = {
    # The default debug_toolbar_middleware.show_toolbar function checks whether the
    # request IP is in settings.INTERNAL_IPS. In Docker, the request IP can vary, so
    # we set it in settings.local instead.
    "SHOW_TOOLBAR_CALLBACK": lambda x: SHOW_TOOLBAR,
    "SHOW_COLLAPSED": True,
}

try:
    from .local import *  # noqa
except ImportError:
    pass
