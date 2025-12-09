
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'dev-secret'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'accounts','farmers','marketplace','payments',
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF = 'agripay.urls'
TEMPLATES = [
    {
        'BACKEND':'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR,'templates')],
        'APP_DIRS':True,
        'OPTIONS':{
            'context_processors':[
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'agripay.wsgi.application'
DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
    }
}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=True
USE_TZ=True
STATIC_URL='/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Daraja API Settings (Sandbox)
DARAJA_CONSUMER_KEY = 'yv5rFJCoqXFUX3qsG5hxyjml4Ko39AzLHRhwtzfb5fJrQq4k'
DARAJA_CONSUMER_SECRET = 'V9fJFGcGTbiRnXRCsMoujkbqIQyo9bBPlY0tmTIIUjdi6PxrAFXwr5PozjVTjsF9'
DARAJA_SHORTCODE = '174379'
DARAJA_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
DARAJA_ENVIRONMENT = 'sandbox'  # Change to 'production' for live

