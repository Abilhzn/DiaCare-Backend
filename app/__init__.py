from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from .core.config import config
from .models.diabetes_prediction_result import db # Mengimpor db dari models.base

bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app) # Untuk mengizinkan request dari Streamlit (beda port)

    # Error Handling Umum
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(error="Bad Request", message=str(error.description if hasattr(error, 'description') else error)), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify(error="Unauthorized", message=str(error.description if hasattr(error, 'description') else error)), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(error="Forbidden", message=str(error.description if hasattr(error, 'description') else error)), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(error="Not Found", message=str(error.description if hasattr(error, 'description') else "The requested URL was not found on the server.")), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        # Sebaiknya log error di sini
        return jsonify(error="Internal Server Error", message="An unexpected error occurred."), 500


    # Registrasi Blueprint untuk setiap fitur
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from .diabetes_prediction.routes import diabetes_prediction_bp
    app.register_blueprint(diabetes_prediction_bp, url_prefix='/api/diabetes')

    from .blood_sugar_monitoring.routes import blood_sugar_bp
    app.register_blueprint(blood_sugar_bp, url_prefix='/api/blood-sugar')

    from .recomendations.routes import recommendations_bp
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')

    from .notifications.routes import notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

    return app