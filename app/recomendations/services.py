from flask import request, jsonify
from . import recommendations_bp
from .services import get_recommendations_for_reading # , get_recommendations_for_diabetes_prediction
from app.core.utils import token_required

# Endpoint ini bisa dipanggil oleh frontend jika ingin mendapatkan rekomendasi secara terpisah,
# atau logikanya bisa langsung dipanggil dari service lain (seperti blood_sugar_monitoring).
# Untuk saat ini, kita asumsikan rekomendasi terintegrasi saat mencatat gula darah.
# Namun, jika ingin ada endpoint khusus:

@recommendations_bp.route('/by-sugar-level', methods=['POST'])
@token_required
def recommend_by_sugar_level_route(current_user): # Contoh endpoint jika diperlukan
    data = request.get_json()
    if not data or 'sugar_level' not in data:
        return jsonify(message="Harap sertakan 'sugar_level' dalam request."), 400
    
    sugar_level = data.get('sugar_level')
    recommendation = get_recommendations_for_reading(sugar_level)
    
    if "tidak valid" in recommendation or "tidak tersedia" in recommendation:
        return jsonify(message=recommendation), 400
        
    return jsonify(recommendation=recommendation), 200

# @recommendations_bp.route('/by-prediction', methods=['POST'])
# @token_required
# def recommend_by_prediction_route(current_user):
#     data = request.get_json()
#     if not data or 'prediction_result' not in data: # Misal 'Tinggi', 'Sedang', 'Rendah'
#         return jsonify(message="Harap sertakan 'prediction_result' dalam request."), 400
    
#     prediction = data.get('prediction_result')
#     recommendation = get_recommendations_for_diabetes_prediction(prediction)
#     return jsonify(recommendation=recommendation), 200