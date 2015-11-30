# for now fetch the development settings only
from dev import *

ALLOWED_HOSTS = ['songbet.me', 'localhost']
DEBUG = False
TEMPLATE_DEBUG = False


ADMINS = (
    ('Igor Pejic', 'igorpejicw@gmail.com'),
)

MANAGERS = ADMINS
