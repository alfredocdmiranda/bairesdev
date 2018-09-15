from .base import *

SECRET_KEY = env('DJANGO_SECRET_KEY', default='yl-b1zikooi(6arkz@p^2#y(@g6fj=mc0ze19*_s1@t1en6=zq')

DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(ROOT_DIR.path('db.sqlite3')),
    }
}