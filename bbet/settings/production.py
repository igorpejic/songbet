# for now fetch the development settings only
from dev import *

STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static/src/spirit/'),
    join(PROJECT_ROOT, 'static/dist/'),
]

ALLOWED_HOSTS = ['songbet.me', 'localhost']
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['songbet.me']


ADMINS = (
    ('Igor Pejic', 'igorpejicw@gmail.com'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'igsmrd@gmail.com'
SERVER_EMAIL = 'igsmrd@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'igsmrd@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_PASSWORD_FILE = normpath(join(PROJECT_ROOT, 'run', 'EMAIL_HOST_PASSWORD.key'))

try:
    EMAIL_HOST_PASSWORD = open(EMAIL_HOST_PASSWORD_FILE).read().strip()
except IOError:
    raise Exception('No EMAIL_HOST_PASSWORD.')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'billboardbet',
        'USER': data['user'],
        'PASSWORD': data['password'],
	'HOST': 'localhost',
	'PORT': ''
    }
}

