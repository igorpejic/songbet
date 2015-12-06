# for now fetch the development settings only
from dev import *

ALLOWED_HOSTS = ['songbet.me', 'localhost']
DEBUG = True
TEMPLATE_DEBUG = True


ADMINS = (
    ('Igor Pejic', 'igorpejicw@gmail.com'),
)

MANAGERS = ADMINS
