from flask import Blueprint, request, jsonify
from app.core.utils import token_required
from app.notifications.services import (
    generate_notification,
    get_user_notifications,
    mark_notification_as_read
)

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

@notifications_bp.route('/', methods=['GET'])
@token_required
def get_notifications_route(current_user):
    """
    Endpoint untuk mengambil semua notifikasi milik user yang sedang login.
    """
    notifications, error_message, status_code = get_user_notifications(current_user)

    if error_message:
        return jsonify({"message": error_message}), status_code
    
    return jsonify(notifications), status_code

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@token_required
def mark_as_read_route(current_user, notification_id):
    """
    Endpoint untuk menandai notifikasi sebagai sudah dibaca.
    """
    updated_notification, message, status_code = mark_notification_as_read(current_user, notification_id)

    if not updated_notification:
        return jsonify({"message": message}), status_code
        
    return jsonify({
        "message": message,
        "notification": updated_notification
    }), status_code
