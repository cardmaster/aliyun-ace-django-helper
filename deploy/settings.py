INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'common.alicache.AliOCSCache',
    },
    'mem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': '######',
        'USER': '#######',
        'PASSWORD': '#######',
        'HOST': '######.mysql.rds.aliyuncs.com',  
        'PORT': '3306',
    }
}


LANGUAGE_CODE = 'zh'

LANGUAGES = (
    ('zh', _('Chinese Simplified')),
    ('en', _('English')),
)


TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/' #although we removed static files middleware, we still need to set this for proper loading of static files for the admin site
LOGIN_REDIRECT_URL = "/"

