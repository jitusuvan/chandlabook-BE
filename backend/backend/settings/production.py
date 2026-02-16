from .base import *
import os
from dotenv import load_dotenv
load_dotenv(override=True)

USER = os.getenv("USER")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")
PASS = os.getenv("PASS")

DEBUG = False
ALLOWED_HOSTS = ["api.jitu007.in", "chandlabook.jitu007.in"]

CORS_ALLOWED_ORIGINS = [ 
    "https://chandlabook.jitu007.in",
]

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': DB,
         'HOST': HOST,
         'PORT': PORT,
         'USER':USER,
         'PASSWORD': PASS
     }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

BASE_URL = os.getenv("BASE_URL")