# Django settings for tbx project.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import dj_database_url

# Configuration from environment variables
env = os.environ.copy()

# On Torchbox servers, many environment variables are prefixed with "CFG_"
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        env[key[4:]] = value

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Basic settings
DEBUG = False

APP_NAME = env.get('APP_NAME', 'torchbox')

if 'SECRET_KEY' in env:
    SECRET_KEY = env['SECRET_KEY']

if 'ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'scout_apm.django',
    'tbx.core.apps.TorchboxCoreAppConfig',

    'wagtail.contrib.search_promotions',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    'wagtailmarkdown',
    'wagtail.contrib.postgres_search',

    'modelcluster',
    'taggit',
    'raven.contrib.django.raven_compat',
    'captcha',
    'wagtailcaptcha',
    'wagtailfontawesome',
    'wagtail_review',

    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'wagtail.contrib.settings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'tbx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tbx.core.context_processors.fb_app_id',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'tbx.wsgi.application'

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# https://github.com/kennethreitz/dj-database-url

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600,
                                      default=f"postgres:///{APP_NAME}")
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'core', 'static_compiled'),
]

STATIC_ROOT = env.get('STATIC_DIR', os.path.join(BASE_DIR, 'static'))
STATIC_URL = env.get('STATIC_URL', '/static/')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files

MEDIA_ROOT = env.get('MEDIA_DIR', os.path.join(BASE_DIR, 'media'))
MEDIA_URL = env.get('MEDIA_URL', '/media/')


# Do not use the same Redis instance for other things like Celery!
if 'REDIS_URL' in env:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env['REDIS_URL'],
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'database_cache',
        }
    }


# Search
# https://docs.wagtail.io/en/latest/topics/search/backends.html

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
    },
}


# S3 configuration
if 'AWS_STORAGE_BUCKET_NAME' in env:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = env['AWS_STORAGE_BUCKET_NAME']
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False

    # You need this to enable signing files. Some old regions may have use a
    # different version than v4.
    AWS_S3_SIGNATURE_VERSION = env.get('AWS_S3_SIGNATURE_VERSION', 's3v4')

    # Set individual files to be private and only allow access to them via
    # bucket policy.
    AWS_DEFAULT_ACL = 'private'

    if 'AWS_S3_SECURE_URLS' in env:
        AWS_S3_SECURE_URLS = (
            env['AWS_S3_SECURE_URLS'].strip().lower() == 'true'
        )

    if 'AWS_S3_ENDPOINT_URL' in env:
        # This setting is required for signing.
        # Please use endpoint from
        # https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
        # e.g. "https://s3.eu-west-2.amazonaws.com"
        AWS_S3_ENDPOINT_URL = env['AWS_S3_ENDPOINT_URL']

    if 'AWS_S3_REGION_NAME' in env:
        # This setting is required for signing.
        AWS_S3_REGION_NAME = env['AWS_S3_REGION_NAME']

    if 'AWS_S3_CUSTOM_DOMAIN' in env:
        AWS_S3_CUSTOM_DOMAIN = env['AWS_S3_CUSTOM_DOMAIN']

    INSTALLED_APPS += (
        'storages',
    )


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Send logs with at least INFO level to the console.
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # Send logs with level of at least ERROR to Sentry.
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s'
        }
    },
    'loggers': {
        '{{ cookiecutter.repo_name }}': {
            'handlers': ['console', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
        'wagtail': {
            'handlers': ['console', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}


# Email settings
if 'EMAIL_HOST' in env:
    EMAIL_HOST = env['EMAIL_HOST']

if 'EMAIL_PORT' in env:
    try:
        EMAIL_PORT = int(env['EMAIL_PORT'])
    except ValueError:
        pass

if 'EMAIL_HOST_USER' in env:
    EMAIL_HOST_USER = env['EMAIL_HOST_USER']

if 'EMAIL_HOST_PASSWORD' in env:
    EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']

if env.get('EMAIL_USE_TLS', 'false').lower().strip() == 'true':
    EMAIL_USE_TLS = True

if env.get('EMAIL_USE_SSL', 'false').lower().strip() == 'true':
    EMAIL_USE_SSL = True

if 'EMAIL_SUBJECT_PREFIX' in env:
    EMAIL_SUBJECT_PREFIX = env['EMAIL_SUBJECT_PREFIX']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = env['SERVER_EMAIL']


# Security configuration
# https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security
if env.get('SECURE_SSL_REDIRECT', 'true').strip().lower() == 'true':
    SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if 'SECURE_HSTS_SECONDS' in env:
    try:
        SECURE_HSTS_SECONDS = int(env['SECURE_HSTS_SECONDS'])
    except ValueError:
        pass

if env.get('SECURE_BROWSER_XSS_FILTER', 'true').lower().strip() == 'true':
    SECURE_BROWSER_XSS_FILTER = True

if env.get('SECURE_CONTENT_TYPE_NOSNIFF', 'true').lower().strip() == 'true':
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer-policy header settings
# https://django-referrer-policy.readthedocs.io/en/1.0/
REFERRER_POLICY = env.get('SECURE_REFERRER_POLICY',
                          'no-referrer-when-downgrade').strip()

# Recaptcha
# https://github.com/springload/wagtail-django-recaptcha
if 'RECAPTCHA_PUBLIC_KEY' in env and 'RECAPTCHA_PRIVATE_KEY' in env:
    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = env['RECAPTCHA_PUBLIC_KEY']
    RECAPTCHA_PRIVATE_KEY = env['RECAPTCHA_PRIVATE_KEY']


# Wagtail settings
WAGTAIL_SITE_NAME = "Torchbox"

FAVICON_STATIC_PATH = 'images/favicon.ico'

if 'PRIMARY_HOST' in env:
    BASE_URL = 'https://{}'.format(env['PRIMARY_HOST'])


# Override the Image class used by wagtailimages with a custom one
WAGTAILIMAGES_IMAGE_MODEL = 'torchbox.TorchboxImage'

# Facebook JSSDK app Id
FB_APP_ID = ''


# Basic auth settings
if env.get('BASIC_AUTH_ENABLED', 'false').lower().strip() == 'true':
    MIDDLEWARE.insert(0, 'baipw.middleware.BasicAuthIPWhitelistMiddleware')
    BASIC_AUTH_LOGIN = env.get('BASIC_AUTH_LOGIN')
    BASIC_AUTH_PASSWORD = env.get('BASIC_AUTH_PASSWORD')
    BASIC_AUTH_WHITELISTED_IP_NETWORKS = [
        # Torchbox networks.
        '78.32.251.192/28',
        '89.197.53.244/30',
        '193.227.244.0/23',
        '2001:41c8:103::/48',
    ]
    if 'BASIC_AUTH_WHITELISTED_HTTP_HOSTS' in env:
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS = (
            env['BASIC_AUTH_WHITELISTED_HTTP_HOSTS'].split(',')
        )


# Front-end cache
# https://docs.wagtail.io/en/latest/reference/contrib/frontendcache.html

if 'FRONTEND_CACHE_PURGE_URL' in env:
    INSTALLED_APPS.append('wagtail.contrib.frontend_cache')
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.frontend_cache.backends.HTTPBackend',
            'LOCATION': env['FRONTEND_CACHE_PURGE_URL'],
        },
    }
elif 'FRONTEND_CACHE_CLOUDFLARE_TOKEN' in env:
    INSTALLED_APPS.append('wagtail.contrib.frontend_cache')
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
            'EMAIL': env['FRONTEND_CACHE_CLOUDFLARE_EMAIL'],
            'TOKEN': env['FRONTEND_CACHE_CLOUDFLARE_TOKEN'],
            'ZONEID': env['FRONTEND_CACHE_CLOUDFLARE_ZONEID'],
        },
    }


# Set s-max-age header that is used by reverse proxy/front end cache. See
# urls.py
try:
    CACHE_CONTROL_S_MAXAGE = int(env.get('CACHE_CONTROL_S_MAXAGE', 600))
except ValueError:
    pass


# Give front-end cache 30 second to revalidate the cache to avoid hitting the
# backend. See urls.py
CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
    env.get('CACHE_CONTROL_STALE_WHILE_REVALIDATE', 30)
)


# Embledly

if 'EMBEDLY_KEY' in env:
    EMBEDLY_KEY = env['EMBEDLY_KEY']


# Newsletter

if 'MAILCHIMP_KEY' in env:
    MAILCHIMP_KEY = env['MAILCHIMP_KEY']

if 'MAILCHIMP_MAILING_LIST_ID' in env:
    MAILCHIMP_MAILING_LIST_ID = env['MAILCHIMP_MAILING_LIST_ID']
