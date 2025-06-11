# app/recommendations/routes.py (Tidak ada perubahan signifikan dari versi sebelumnya)

from flask import Blueprint, request, jsonify
from app.recomendations.services import get_recommendation_service

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/get_recommendation', methods=['POST'])
def get_recommendation_route():
    """
    Endpoint untuk mendapatkan rekomendasi tindakan berdasarkan data glukosa.
    Menerima data JSON:
    {
        "age": int,
        "glucose": int,
        "condition": "sebelum" | "sesudah", # Ini akan dikirim dari modul pemantauan atau sudah diproses sebelumnya
        "category": "sehat" | "pradiabetes" | "diabetes"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Permintaan tidak valid, harap kirimkan data JSON."}), 400

    age = data.get('age')
    glucose = data.get('glucose')
    condition = data.get('condition')
    category = data.get('category')

    # Basic input validation from route level (can be expanded)
    if not all([age is not None, glucose is not None, condition, category]):
        return jsonify({"status": "error", "message": "Data input tidak lengkap (age, glucose, condition, category diperlukan)."}), 400
    
    if not isinstance(age, int) or age <= 0:
        return jsonify({"status": "error", "message": "Usia tidak valid."}), 400

    # Panggil service untuk mendapatkan rekomendasi
    result = get_recommendation_service(age, glucose, condition, category)

    if result["status"] == "success":
        return jsonify(result), 200
    elif result["status"] == "warning": # Untuk Hipoglikemia/Hiperglikemia ekstrem
        return jsonify(result), 200 
    else: # status == "error"
        return jsonify(result), 400