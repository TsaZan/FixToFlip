from datetime import timedelta
from pathlib import Path

import os
from dotenv import load_dotenv
import dj_database_url
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
import mimetypes
import json

config = cloudinary.config(secure=True)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_USER_MODEL = 'accounts.BaseAccount'
DEBUG = bool(int(os.getenv('DEBUG', 0)))

CSRF_COOKIE_SECURE = False

RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

ALLOWED_HOSTS = os.getenv('HOSTS_ALLOWED').split(',')

PROJECT_APPS = [
    'FixToFlip.accounts',
    'FixToFlip.credits',
    'FixToFlip.properties',
    'FixToFlip.offers',
    'FixToFlip.common',
    'FixToFlip.dashboard',
    'FixToFlip.blog',
]

AUTHENTICATION_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',
    'allauth.socialaccount.providers.google', ]

THIRD_PARTY_APPS = [
    'djmoney',
    'djmoney.contrib.exchange',
    'cloudinary',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'cities_light',
    'django_recaptcha',
    'whitenoise.runserver_nostatic',
    "phonenumber_field",
    'django_celery_beat',

]

INSTALLED_APPS = [
                     'unfold',
                     'unfold.contrib.filters',
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.sites',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',

                     'django.contrib.sitemaps'
                 ] + PROJECT_APPS + THIRD_PARTY_APPS + AUTHENTICATION_APPS

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'

    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Allauth middleware:
    "allauth.account.middleware.AccountMiddleware",
]
#ANOTHER EXCHANGE RATES - Fixer.io
# EXCHANGE_BACKEND = 'djmoney.contrib.exchange.backends.FixerBackend'
#FIXER_ACCESS_KEY = os.getenv('FIXER_API_KEY')

SERIALIZATION_MODULES = {"json": "djmoney.serializers"}
OPEN_EXCHANGE_RATES_APP_ID = os.getenv('EXCHANGE_RATE_API_KEY')
DJANGO_MONEY_RATES = {
    'DEFAULT_BACKEND': 'djmoney.contrib.exchange.backends.OpenExchangeRatesBackend',
    'OPENEXCHANGERATES_URL': 'https://openexchangerates.org/api/latest.json',
    'OPENEXCHANGERATES_APP_ID': os.getenv('EXCHANGE_RATE_API_KEY'),
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_URLS').split(',')
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
ALLOWED_DOMAIN = ALLOWED_HOSTS

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_AUTO_SIGN_UP = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[FixToFlip] "
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = '/dashboard/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ],
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        },
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
}

ROOT_URLCONF = 'FixToFlip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'FixToFlip.common.context_processor.login_ctx.login_ctx_tag',
                'FixToFlip.common.context_processor.login_ctx.signup_ctx_tag',
                'FixToFlip.common.context_processor.login_ctx.preloader_context',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 1

WSGI_APPLICATION = 'FixToFlip.wsgi.application'

DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL', None))}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR / 'staticfiles/',
)

STATIC_ROOT = BASE_DIR / 'static'

CURRENCIES = ('EUR',)

DEFAULT_CURRENCY = 'EUR'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

CELERY_BROKER_URL = os.getenv('BROKER_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_IMPORTS = (
    'FixToFlip.common.task',
)
