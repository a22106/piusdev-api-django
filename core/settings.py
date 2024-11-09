import os
import random
import string
import sys
from pathlib import Path

from dotenv import load_dotenv

from django.db import connections
from django.db.utils import OperationalError


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(32))

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "piusdev-qrcode-9f0c9f745f56.herokuapp.com",
    "qrcode.piusdev.com",
    "localhost",
    "127.0.0.1",
]


if not DEBUG:
    ALLOWED_HOSTS += os.environ.get("ALLOWED_HOSTS", "").split(",")

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5085",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5085",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    "core",
    "qr_auth",
    "qr",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap5",
    "drf_yasg",
    "rest_framework",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "core.urls"

HOME_TEMPLATES = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [HOME_TEMPLATES],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SUPABASE_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SUPABASE_DB_NAME", "postgres"),
        "USER": os.environ.get("SUPABASE_DB_USER", "postgres"),
        "PASSWORD": os.environ.get("SUPABASE_DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("SUPABASE_DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("SUPABASE_DB_PORT", "54322"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
}

# Supabase Settings
SUPABASE_API_URL = os.environ.get("SUPABASE_URL", "http://127.0.0.1:54321")
SUPABASE_GRAPHQL_URL = os.environ.get(
    "SUPABASE_GRAPHQL_URL", "http://127.0.0.1:54321/graphql/v1"
)
SUPABASE_S3_STORAGE_URL = os.environ.get(
    "SUPABASE_S3_STORAGE_URL", "http://127.0.0.1:54321/storage/v1/s3"
)
SUPABASE_DB_URL = os.environ.get(
    "SUPABASE_DB_URL", "postgresql://postgres:postgres@127.0.0.1:54322/postgres"
)
SUPABASE_STUDIO_URL = os.environ.get("SUPABASE_STUDIO_URL", "http://127.0.0.1:54323")
SUPABASE_INBUCKET_URL = os.environ.get(
    "SUPABASE_INBUCKET_URL", "http://127.0.0.1:54324"
)
SUPABASE_JWT_SECRET = os.environ.get(
    "SUPABASE_JWT_SECRET", "super-secret-jwt-token-with-at-least-32-characters-long"
)
SUPABASE_ANON_KEY = os.environ.get(
    "SUPABASE_ANON_KEY",
)
SUPABASE_SERVICE_ROLE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY",
)
SUPABASE_S3_ACCESS_KEY = os.environ.get(
    "SUPABASE_S3_ACCESS_KEY", "625729a08b95bf1b7ff351a663f3a23c"
)
SUPABASE_S3_SECRET_KEY = os.environ.get(
    "SUPABASE_S3_SECRET_KEY",
    "850181e4652dd023b7a98c58ae0d2d34bd487ee0cc3254aed6eda37307425907",
)
SUPABASE_S3_REGION = os.environ.get("SUPABASE_S3_REGION", "local")


try:
    connections["default"].cursor()
except OperationalError:
    print("데이터베이스 연결 실패")
    sys.exit(1)
