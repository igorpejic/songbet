# Import some utility functions
from os.path import join
# Fetch our common settings
import json

from common import *
from spirit.settings import *

# #########################################################

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

DB_FILE = normpath(join(PROJECT_ROOT, 'run', 'DB.json'))

with open(DB_FILE) as f:
    data = json.load(f)


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'billboardbet',
        'USER': data['user'],
        'PASSWORD': data['password'],
    }
}

# ##### APPLICATION CONFIGURATION #########################

# This is because of spirit

INSTALLED_APPS = DEFAULT_APPS + list(set(INSTALLED_APPS) - set(DEFAULT_APPS))
INSTALLED_APPS += ('django_extensions',)

# Override spirit
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    MIDDLEWARE_CLASSES + list(set(COMMON_MIDDLEWARE_CLASSES) - set(MIDDLEWARE_CLASSES))
)
