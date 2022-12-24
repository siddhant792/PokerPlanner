import os

from class_settings import Settings


class Setting(Settings):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = 'bf#3+((2_t_-h0nt4k#)5md1rl%8p$o^*!k0+1v_^rb*j36(6g'

    DEBUG = False

    ALLOWED_HOSTS = []

    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    LOCAL_APPS = [
        'apps.pokerboard.app_config.PokerboardConfig',
        'apps.group.app_config.GroupConfig',
        'apps.user.app_config.UserConfig',
    ]

    THIRD_PARTY_APPS = [
        'corsheaders',
        'rest_framework',
        'channels',
    ]

    INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

    AUTH_USER_MODEL = 'user.User'

    CORS_ORIGIN_ALLOW_ALL = True

    AUTH_GROUP = None

    TOKEN_TTL = 500

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'corsheaders.middleware.CorsMiddleware',
    ]

    ROOT_URLCONF = 'poker.urls'

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

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            "apps.user.authentication.CustomTokenAuthentication",
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            "rest_framework.permissions.IsAuthenticated",
        ],
    }

    ASGI_APPLICATION = "poker.asgi.application"

    WSGI_APPLICATION = "poker.wsgi.application"

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

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydatabase',
        }
    }

    CHANNEL_LAYERS = {
        'default': {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Asia/Kolkata'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = False

    STATIC_URL = '/static/'
