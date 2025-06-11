from flask import request, jsonify
from . import diabetes_prediction_bp
from .services import predict_diabetes_service
from app.core.utils import token_required

@diabetes_prediction_bp.route('/predict', methods=['POST'])
@token_required
def predict_route(current_user):
    data = request.get_json()
    if not data:
        return jsonify(message="Request body harus JSON."), 400

    # Panggil logic utama di services.py (gate MUA)
    response = predict_diabetes_service(current_user, data)

    # Pastikan response dari service sudah konsisten: dict dengan kunci 'result' dan/atau 'error'
    if 'error' in response:
        return jsonify(message=response['error']), 400

    return jsonify(response['result']), 200
