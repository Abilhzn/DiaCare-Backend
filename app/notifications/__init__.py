# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # --- Register Blueprints ---
    from app.recomendations.routes import recommendations_bp
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')

    from app.notifications.routes import notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

    return app