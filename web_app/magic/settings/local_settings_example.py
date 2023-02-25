ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "magic_local",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
