# Import sys (to adjust Python path)
import sys
import datetime
# Import some utility functions
from os.path import abspath, basename, dirname, join, normpath

# #########################################################

# ##### PATH CONFIGURATION ################################

# Fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# The name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# Collect static files here
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')

# Collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

VAR_ROOT = join(PROJECT_ROOT, 'var')
IMAGE_ASSETS = join(VAR_ROOT, 'image_assets')
VIDEO_ASSETS = join(VAR_ROOT, 'video_assets')
RAW_VIDEOS = join(VAR_ROOT, 'raw_videos')

IMAGES = join(VAR_ROOT, 'images')
VIDEOS = join(VAR_ROOT, 'videos')

# look for static assets here
# overriden in production
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]


# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'static/src'),
]

# Add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))


# ##### APPLICATION CONFIGURATION #########################

# This are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'apps.bet',
    'apps.image',
    'apps.video',
    'django_nose',
    'spirit',
    'lazysignup'
]

# Middlewares
COMMON_MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

# Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'lazysignup.backends.LazySignupBackend',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '609163425136-1i7b7jlr4j4hlqtnb1gk3al2kagavcjm.apps.googleusercontent.com'  # noqa
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = '1629513813961116'
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

GOOGLE_API_KEY = ''

# Template stuff
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

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))
GOOGLE_SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'GOOGLE_SECRET.key'))
FACEBOOK_SECRET_FILE = normpath(join(PROJECT_ROOT, 'run',
                                     'FACEBOOK_SECRET.key'))

GOOGLE_API_KEY_FILE = normpath(join(PROJECT_ROOT, 'run',
                                    'GOOGLE_API.key'))

# These persons receive error notification
ADMINS = (
    ('your name', 'your_name@example.com'),
)
MANAGERS = ADMINS


# ##### DJANGO RUNNING CONFIGURATION ######################

# The default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# The root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# This site's ID
SITE_ID = 1

# The URL for static files
STATIC_URL = '/static/'

# The URL for media files
MEDIA_URL = '/media/'


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True


# ##### INTERNATIONALIZATION ##############################

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Berlin'

# Internationalization
USE_I18N = True

# Localisation
USE_L10N = True

# enable timezone awareness by default
USE_TZ = True


# Finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)
try:
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = open(GOOGLE_SECRET_FILE).read().strip()
except IOError:
    raise Exception('No GOOGLE_SECRET_FILE.')

try:
    SOCIAL_AUTH_FACEBOOK_SECRET = open(FACEBOOK_SECRET_FILE).read().strip()
except IOError:
    raise Exception('No FACEBOOK_SECRET_FILE.')

try:
    GOOGLE_API_KEY = open(GOOGLE_API_KEY_FILE).read().strip()
except IOError:
    raise Exception('No GOOGLE_API_KEY_FILE.')

# ##### DJANGO REST FRAMEWORK ##############################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',

    # wait until satellizer implements token refresh
    'JWT_EXPIRATION_DELTA': datetime.timedelta(weeks=2),
}

