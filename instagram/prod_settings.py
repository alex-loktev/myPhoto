# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

from .settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'insta',
        'USER': 'shmarovoz',
        'PASSWORD': 'jw0r425m',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


SECRET_KEY = '*ls7+%-nt5!=cye9m1(n&#h-1_%^(519r9b6ez@obydysfmbso'
