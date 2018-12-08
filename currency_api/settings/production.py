from .base import *  # noqa
import os


DEBUG = False
SECRET_KEY = '$^&118i$9u9n)y915cwj6&*m@doctf&2r53j!572sey930gw*h'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
ALLOWED_HOSTS = ALLOWED_HOSTS + ['web']

ADMINS = (
    ('Roberto Pomoni', 'roberto.pomoni@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'currency_api.db',
    }
}
