import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Konfigurasi dasar yang akan diwarisi oleh konfigurasi lainnya.
    """
    # Kunci rahasia untuk keamanan sesi dan CSRF.   
    SECRET_KEY = os.environ.get('joelsiboedaksby') or 'joelsiboedaksby'

    # Menonaktifkan fitur modifikasi dari SQLAlchemy yang tidak diperlukan dan deprecated.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Kunci rahasia untuk JSON Web Tokens (JWT).
    JWT_SECRET_KEY = os.environ.get('benjowel') or 'benjowel'

    MODEL_PATH = os.path.join(basedir, 'app', 'diabetes_prediction', 'ml_model', 'diabetes_model.pkl')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    # Mengaktifkan mode debug Flask untuk hot-reloading dan debugger interaktif.
    DEBUG = True

    # URI untuk database pengembangan.
    # Menggunakan SQLite agar mudah untuk memulai.
    # File database (diacare_dev.db) akan dibuat di direktori root proyek.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'diacare_dev.db')

class TestingConfig(Config):
    # Mengaktifkan mode testing Flask.
    TESTING = True

    # Menonaktifkan CSRF protection dalam form saat testing.
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///:memory:'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'diacare.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
