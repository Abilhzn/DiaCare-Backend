from flask import Blueprint, request, jsonify
from app.notifications.services import generate_notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/send', methods=['POST'])
def send_notification():
    """
    Endpoint untuk mengirim notifikasi berdasarkan hasil rekomendasi.
    Menerima data JSON:
    {
        "age": int,
        "glucose": int,
        "condition": "sebelum" | "sesudah",
        "category": "sehat" | "pradiabetes" | "diabetes"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Data tidak ditemukan atau tidak dalam format JSON."}), 400

    age = data.get("age")
    glucose = data.get("glucose")
    condition = data.get("condition")
    category = data.get("category")

    if not all([age, glucose, condition, category]):
        return jsonify({"status": "error", "message": "Parameter tidak lengkap."}), 400

    result = generate_notification(age, glucose, condition, category)

    return jsonify(result), 200 if result["status"] in ["success", "warning"] else 400
