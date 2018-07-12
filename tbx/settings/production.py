from .base import *  # noqa

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False


# Facebook JSSDB app id
FB_APP_ID = '323944607389'


try:
    from .local import *  # noqa
except ImportError:
    pass
