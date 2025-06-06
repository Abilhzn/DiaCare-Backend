from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # Umumnya digunakan bersama SQLAlchemy
from flask_jwt_extended import JWTManager # Karena ada JWT_SECRET_KEY di config
# Import konfigurasi yang telah Anda buat
from config import config # Asumsi config.py berada di root direktori, sejajar dengan run.py

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

    # Registrasi Blueprint
    # Pastikan path import sesuai dengan struktur proyek Anda
    # Contoh: from .auth.routes import auth_bp
    # (Anda perlu membuat direktori 'auth' dan file 'routes.py' di dalamnya)
    
    # --- AUTH BLUEPRINT ---
    # Cek apakah direktori app/auth ada sebelum mencoba import
    # Ini untuk menghindari error jika blueprint belum dibuat
    try:
        from .auth.routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
    except ImportError:
        # Anda bisa menambahkan logging di sini jika blueprint auth tidak ditemukan
        # misalnya app.logger.warning("Auth blueprint not found or not yet created.")
        pass # Lanjutkan jika blueprint auth belum ada

    # --- BLOOD SUGAR MONITORING BLUEPRINT (Contoh) ---
    # try:
    #     from .blood_sugar_monitoring.routes import blood_sugar_bp 
    #     app.register_blueprint(blood_sugar_bp, url_prefix='/blood_sugar')
    # except ImportError:
    #     pass

    # --- DIABETES PREDICTION BLUEPRINT (Contoh) ---
    # try:
    #     from .diabetes_prediction.routes import prediction_bp
    #     app.register_blueprint(prediction_bp, url_prefix='/predict')
    # except ImportError:
    #     pass
        
    # --- NOTIFICATIONS BLUEPRINT (Contoh) ---
    # try:
    #     from .notifications.routes import notifications_bp
    #     app.register_blueprint(notifications_bp, url_prefix='/notifications')
    # except ImportError:
    #     pass

    # --- RECOMMENDATIONS BLUEPRINT (Contoh) ---
    # try:
    #     from .recommendations.routes import recommendations_bp
    #     app.register_blueprint(recommendations_bp, url_prefix='/recommendations')
    # except ImportError:
    #     pass

    # Tambahkan rute sederhana untuk pengujian jika diperlukan
    @app.route('/hello')
    def hello():
        return 'Hello, World! App is running with {} config.'.format(config_name)

    return app

# Anda mungkin juga ingin menambahkan file models.py di root app jika ada model global
# atau pastikan semua model diimpor di tempat yang tepat agar dikenali oleh Flask-Migrate.
# Contoh:
# from . import models # jika ada app/models.py
# from .auth import models as auth_models # jika model ada di dalam setiap blueprint
