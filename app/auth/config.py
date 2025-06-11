import os

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dia_care.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_default_jwt_secret_key'

    @staticmethod
    def init_app(app):
        pass  # Bisa diisi konfigurasi tambahan jika diperlukan

class DevelopmentConfig(config):
    DEBUG = True

class ProductionConfig(config):
    DEBUG = False

class TestingConfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}