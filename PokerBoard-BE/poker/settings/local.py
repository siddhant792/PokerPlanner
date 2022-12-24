from poker.settings.base import Setting

class Setting(Setting):
    # ALLOWED_HOSTS = ['localhost',]
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'pokerplanner',
            'USER': 'postgres',
            'PASSWORD': 'Manchd@123',
        }
    }

    CELERY_BROKER_URL = 'amqp://localhost'
    
    BASE_URL_FE = '127.0.0.1:8080/#'

    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'testformailsmtp@gmail.com'
    EMAIL_HOST_PASSWORD = 'hbgotxmqasfsahfs'

    JIRA_AUTH_USERNAME = 'siddhantgupta792000@gmail.com'
    JIRA_AUTH_TOKEN = "rFjIMF2LZqtDEQCtwASK642C"
    JIRA_URL = "https://pokerplannermajor.atlassian.net/"
