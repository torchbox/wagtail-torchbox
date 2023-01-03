from .base import *  # noqa

# Don't redirect to HTTPS in tests.
SECURE_SSL_REDIRECT = False

# Don't insist on having run birdbath
BIRDBATH_REQUIRED = False

# By default, Django uses a computationally difficult algorithm for passwords hashing.
# We don't need such a strong algorithm in tests, so use MD5
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
