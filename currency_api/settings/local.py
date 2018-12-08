from .base import *  # noqa

DEBUG = True

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

