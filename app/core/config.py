import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'joelsiboedaksby'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'benjowel'
    
    # Biarkan ini kosong, kita akan isi di __init__.py
    SQLALCHEMY_DATABASE_URI = None 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # DATABASE_URL_FROM_ENV = os.getenv('DATABASE_URL')
    # if not DATABASE_URL_FROM_ENV:
    #     raise RuntimeError("FATAL ERROR: DATABASE_URL environment variable tidak ditemukan atau kosong. Pastikan ada di file .env")
    
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = DATABASE_URL_FROM_ENV
    # print(f"--- [CONFIG] Nilai SQLALCHEMY_DATABASE_URI dibaca sebagai: {SQLALCHEMY_DATABASE_URI}")
    
    # Untuk model ML
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'diabetes_prediction', 'ml_model', 'diabtes_predicition_model.pkl')


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('postgresql://neondb_owner:npg_iuBV4UwnXgd7@ep-lingering-smoke-a8k2u48j-pooler.eastus2.azure.neon.tech/neondb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('postgresql://neondb_owner:npg_iuBV4UwnXgd7@ep-lingering-smoke-a8k2u48j-pooler.eastus2.azure.neon.tech/neondb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('postgresql://neondb_owner:npg_iuBV4UwnXgd7@ep-lingering-smoke-a8k2u48j-pooler.eastus2.azure.neon.tech/neondb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}