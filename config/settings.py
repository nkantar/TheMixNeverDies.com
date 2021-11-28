"""
Django settings for tmnd project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""


from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c!qdpge@k-a=4b6q&=os5n!en4ab1@^*8d$nkz9f-=$a(seq4*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "tmnd.local",
    ".tmnd.local",
    "themixneverdies.com",
    ".themixneverdies.com",
]


# Application definition

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.spotify",
    "django_rq",
    # project
    "tmnd.core",
    "tmnd.main",
    "tmnd.cms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tmnd.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


##################################################
##################################################
##################################################
##################################################
##################################################


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPES = [
    "user-read-email",  # default from django-allauth
    "playlist-modify-public",
    "user-library-read",
]
SOCIALACCOUNT_PROVIDERS = {
    "spotify": {
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
        "SCOPE": SPOTIFY_SCOPES,
    },
}

APPEND_SLASH = True

STATIC_ROOT = "static/"
STATICFILES_DIRS = []

RQ_QUEUES = {
    "default": {
        "HOST": "redis",
        "PORT": 6379,
        "DB": 0,
        "PASSWORD": getenv("REDIS_PASSWORD"),
    }
}

if DEBUG:
    SCHEME = "http"
    DOMAIN = "tmnd.local"
    PORT = ":8000"
else:
    SCHEME = "https"
    DOMAIN = "themixneverdies.com"
    PORT = ""

MAIN_PATH = f"{SCHEME}://{DOMAIN}{PORT}"
LOGIN_REDIRECT_URL = f"{MAIN_PATH}/user/"  # TODO use main domain
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_ON_GET = True

SESSION_COOKIE_DOMAIN = f".{DOMAIN}"

LOGIN_PATH = f"{MAIN_PATH}/accounts/spotify/login/?process=login"
LOGOUT_PATH = f"{MAIN_PATH}/accounts/logout/"

PAGE_SIZE = 10

ACCOUNT_EMAIL_VERIFICATION = "none"