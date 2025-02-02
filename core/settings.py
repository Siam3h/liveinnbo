from pathlib import Path
import os
from decouple import config
import datetime


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insexfregstbynt thbfa\zsdxfcgvhbjnbvccure-+r480m@z6_x@hh4w#fq6t8zqrfo8+d@2823@eu7vntl!cz=%o'

# Paystack credentials
PAYSTACK_PUBLIC_KEY = "sk_test_dbfb14cbdd52ae1ff047db500381b9583d379666"
PAYSTACK_SECRET_KEY = "sk_test_dbfb14cbdd52ae1ff047db500381b9583d379666"

PAYSTACK_BASE_URL = "https://api.paystack.co"

GOOGLE_OAUTH_CLIENT_ID="830795346343-7uajlpulc4tne0f07vt39hlg0ie0n82l.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET="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"
FACEBOOK_APP_ID="881321644102910"
FACEBOOK_APP_SECRET="96c5b0b938024e293021b932f4b8804f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # For testing; restrict this in production

CSRF_TRUSTED_ORIGINS = ['*']

# Application definition
INSTALLED_APPS = [
    'social_django',
    'blogs',
    'accounts',
    'events',
    'newsletters',
    'payments',
    'app_theme',
    'tailwind',
    'tinymce',
    'home.apps.HomeConfig',
    'django_browser_reload',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Tailwind and Browser Reload Settings
TAILWIND_APP_NAME = 'app_theme'
INTERNAL_IPS = ["127.0.0.1"]
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

# Middleware
MIDDLEWARE = [
    'accounts.middleware.JWTAuthenticationMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configurations
ROOT_URLCONF = 'core.urls'

# settings.py

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/auth/user/admin/' 
SOCIAL_AUTH_LOGOUT_REDIRECT_URL = '/auth/login/'  


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

# WSGI application
WSGI_APPLICATION = 'core.wsgi.application'

# Database configuration (use one at a time)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media files
STATIC_URL = '/static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Static file settings for production
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'philosiama@gmail.com'

# Authentication backends and OAuth keys
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# OAuth credentials 
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_OAUTH_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_OAUTH_CLIENT_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = config('FACEBOOK_APP_ID')
SOCIAL_AUTH_FACEBOOK_SECRET = config('FACEBOOK_APP_SECRET')

SECRET_KEY = 'nhggftt566433waq234trt'
JWT_SECRET = '78uhhffvbcxzaqwegioolmn'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600  # 1 hour expiry