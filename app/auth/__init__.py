from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import config 

# Inisialisasi ekstensi tanpa aplikasi terlebih dahulu
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager() # Inisialisasi JWTManager

def create_app(config_name='default'):
    """
    Factory function untuk membuat instance aplikasi Flask.
    :param config_name: Nama konfigurasi yang akan digunakan (misalnya, 'development', 'production').
    """
    app = Flask(__name__)

    # Muat konfigurasi dari objek config berdasarkan config_name
    # Jika config_name tidak ditemukan, akan menggunakan 'default' dari dictionary config
    app.config.from_object(config.get(config_name, config['default']))
    
    # Panggil metode init_app dari objek config jika ada (sesuai struktur config.py Anda)
    config[config_name].init_app(app)

    # Inisialisasi ekstensi dengan aplikasi
    db.init_app(app)
    migrate.init_app(app, db) # Inisialisasi Flask-Migrate
    jwt.init_app(app) # Inisialisasi Flask-JWT-Extended

    try:
        from auth.routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
    except ImportError:
        pass 

    @app.route('/hello')
    def hello():
        return 'Hello, World! App is running with {} config.'.format(config_name)

    return app

