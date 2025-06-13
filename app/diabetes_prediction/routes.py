from flask import request, jsonify
from . import diabetes_prediction_bp
from .services import predict_diabetes_service
from app.core.utils import token_required

@diabetes_prediction_bp.route('/predict', methods=['POST'])
@token_required
def predict_route(current_user):
    """
    Endpoint untuk menerima data dan mengembalikan prediksi risiko diabetes.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body harus dalam format JSON."}), 400
    
    risk_level, recommendation, error_message, status_code = predict_diabetes_service(current_user, data)

    # Pastikan response dari service sudah konsisten: dict dengan kunci 'result' dan/atau 'error'
    if error_message:
        return jsonify({"message": error_message}), status_code
    
    return jsonify({
        "risk_level": risk_level,
        "recommendation": recommendation
    }), status_code