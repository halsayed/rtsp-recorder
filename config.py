import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_HOST = 'localhost'


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    REDIS_HOST = 'localhost'


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig(),
    'testing': TestConfig(),
    'production': ProductionConfig(),

    'default': DevelopmentConfig()
}