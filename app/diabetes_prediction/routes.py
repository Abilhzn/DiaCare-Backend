from flask import request, jsonify
from . import diabetes_prediction_bp
from .services import predict_diabetes_service
from app.core.utils import token_required # Untuk proteksi endpoint

@diabetes_prediction_bp.route('/predict', methods=['POST'])
@token_required
def predict_route(current_user): # current_user didapat dari @token_required
    data = request.get_json()
    if not data:
        return jsonify(message="Request body harus JSON."), 400

    # Skenario SC006: Prediksi risiko berdasarkan input valid [cite: 12]
    # Skenario SC007: Gagal prediksi karena data tidak lengkap [cite: 12]
    # Skenario SC008: Validasi input numerik [cite: 12]
    # Skenario SC009: Estimasi risiko tinggi sesuai data input [cite: 12]
    # Skenario SC010: Estimasi risiko rendah sesuai data input [cite: 12]
    result, error_message = predict_diabetes_service(current_user, data)

    if error_message:
        # SC007 & SC008 akan ditangani di sini
        return jsonify(message=error_message), 400 
    
    # SC006, SC009, SC010 akan menghasilkan result
    return jsonify(result), 200