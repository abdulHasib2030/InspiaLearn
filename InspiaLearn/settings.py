"""
Django settings for InspiaLearn project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*o-mjxy_3mzcd5c2*ov1d8h_7wmatcwc&2@mx6@lfx13t==e-r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


     ## custom app
    'accounts',
    'category',
    'instructor',
    'learner',
# "whitenoise.runserver_nostatic",

]
import dj_database_url
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'InspiaLearn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'InspiaLearn.wsgi.application'

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# import dj_database_url
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://inspialearn_user:6uZ18cLcsgzSjF3wzBG8icDnUKSebTOB@dpg-ctc2ott2ng1s73bt6t8g-a.singapore-postgres.render.com/inspialearn',
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
# api/settings.py


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATIC_URL = 'static/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
# STATICFILES_DIRS =  [
#     BASE_DIR/'static',
# ]

if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


<<<<<<< HEAD
import environ
import os
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DEBUG = env('DEBUG')
GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID_")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET_")
GOOGLE_REDIRECT_URI = env("GOOGLE_REDIRECT_URI_")

=======
# import environ
# import os
# env = environ.Env(
#     DEBUG=(bool, False)
# )
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# DEBUG = env('DEBUG')
# GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID_")
# GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET_")
# # GOOGLE_REDIRECT_URI = env("GOOGLE_REDIRECT_URI_")

# GOOGLE_REDIRECT_URI= 'https://inspialearn.onrender.com/oauth2callback/'
GOOGLE_CLIENT_ID = '320501578879-eefjqaoj6idbdhdbramtis16hp63t1v0.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'https://inspialearn.onrender.com/oauth2callback/'
>>>>>>> 46b76030c669c5d45daa57ea8b66117ceb394732
