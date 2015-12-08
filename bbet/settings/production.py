# for now fetch the development settings only
from dev import *

ALLOWED_HOSTS = ['songbet.me', 'localhost']
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['songbet.me']


ADMINS = (
    ('Igor Pejic', 'igorpejicw@gmail.com'),
)

MANAGERS = ADMINS

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'igorpejicw@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
