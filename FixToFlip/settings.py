from datetime import timedelta
from pathlib import Path

import os
from dotenv import load_dotenv
import dj_database_url
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
import json

config = cloudinary.config(secure=True)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = ['*', ]

PROJECT_APPS = [
    'FixToFlip.accounts',
    'FixToFlip.calculator',
    'FixToFlip.credits',
    'FixToFlip.properties',
    'FixToFlip.notifications',
    'FixToFlip.offers',
    'FixToFlip.common',
    'FixToFlip.dashboard',
    'FixToFlip.blog',
]

AUTHENTICATION_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.openid_connect',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_ON_GET = True

THIRD_PARTY_APPS = [
    'djmoney',
    'djmoney.contrib.exchange',
    'cloudinary',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # За токен базирано удостоверяване
        'rest_framework.authentication.SessionAuthentication',  # Ако използвате сесии
        #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}
INSTALLED_APPS = [
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',

                     'django.contrib.sitemaps'
                 ] + PROJECT_APPS + THIRD_PARTY_APPS + AUTHENTICATION_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CSRF_TRUSTED_ORIGINS = ['http://*.127.0.0.1']
ALLOWED_DOMAIN = '127.0.0.1'
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGN_UP = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = "none"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
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
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
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

STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

STATIC_URL = 'static/'

STATICFILES_DIRS = (
    BASE_DIR / 'staticfiles/',
)

STATIC_ROOT = BASE_DIR / 'static'
CURRENCIES = ('USD', 'EUR', 'GBP', 'BGN', 'AED', 'CHF')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import mimetypes

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)
