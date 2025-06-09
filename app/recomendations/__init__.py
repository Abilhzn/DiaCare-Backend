from flask import Flask

def create_app():
    app = Flask(__name__)

    # --- Register Blueprints ---
    from app.recommendations.routes import recommendations_bp
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')

    return app
