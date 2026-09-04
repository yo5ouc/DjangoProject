import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/radio/"
LOGOUT_REDIRECT_URL = "/admin/login/"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'local-development-secret-key')
DEBUG = True
ALLOWED_HOSTS = [
    "yo5ouc.remoteusb.org",
    ".remoteusb.org",
    ".onrender.com",
    "localhost",
    "127.0.0.1",
]
USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
    'daphne',  # Must be first for ASGI/Channels support
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    # Add your core app here:
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CSRF_TRUSTED_ORIGINS = [
    "https://yo5ouc.remoteusb.org",
    "https://*.remoteusb.org",       # Covers any other subdomains
    "https://*.onrender.com",        # Useful for default Render subdomains
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
APPEND_SLASH = False