import os.path

INSTALLED_APPS = [
    'nap',
    'polls',
]

SITE_ID = 1
SECRET_KEY = '+zzix-&k$afk-k0d0s7v01w0&15z#ne$71qf28#e$$c*@g742z'
ROOT_URLCONF = "urls"

DEBUG = True

STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'database.db'),
    }
}
