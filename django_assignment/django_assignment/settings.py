from pathlib import Path
from django.conf.urls.static import static
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-ed*765rxcymxl#5(s@!5_!e!z&mpdr1vlv&80_vqe*7q^&4%1y'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_assignment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'django_assignment.wsgi.application'
PASSWORD = os.getenv('PASSWORD', 'p@stgress')
HOST = os.getenv('HOST', 'localhost')
DATABASE = os.getenv('DJANGO_DATABASE', 'django_database')
USERNAME = os.getenv('DB_USER', 'postgres')
PORT = os.getenv('PORT', '5433')



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE,     
        'USER': USERNAME,          
        'PASSWORD': PASSWORD,     
        'HOST': HOST,               
        'PORT': PORT                   
    }
}


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


STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
# http://127.0.0.1:8000/media/property_images/Burj_arab.jpg
# /home/w3e11/Desktop/Django-Admin_Assignment/django_assignment/media/property_images/1mc3f12000d272kqk5CF8_R_250_250_R5_D.jpg
# http://127.0.0.1:8000/media/property_images/1mc3f12000d272kqk5CF8_R_250_250_R5_D.jpg

