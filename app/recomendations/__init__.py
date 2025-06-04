# app/__init__.py (contoh, sesuaikan dengan inisialisasi aplikasi Anda)

from flask import Flask

def create_app():
    app = Flask(__name__)

    # --- Register Blueprints ---
    from app.recomendations.routes import recommendations_bp
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations') # Contoh prefix URL
    
    # Anda juga perlu mendaftarkan blueprint lain di sini:
    # from app.auth.routes import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # ... dll

    return app