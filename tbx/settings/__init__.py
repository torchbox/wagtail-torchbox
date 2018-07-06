# If you want to avoid weird side effects, do not import dev settings here.
# For example, if your dev settings do something like
#
#    INSTALLED_APPS += [
#       'debug_toolbar',
#    ]
#
# You will have `debug_toolbar` enabled even if you run
# your application in production settings because `INSTALLED_APPS` will be changed during import
#
# It's better to explicitly specify settings file
# by setting the `DJANGO_SETTINGS_MODULE` environment variable
# or passing the --settings argument into your manage commands, when possible.
