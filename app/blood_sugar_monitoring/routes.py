# DIACARE-BACKEND/app/blood_sugar_monitoring/routes.py

from flask import Blueprint, request, jsonify
from .services import add_blood_sugar_service, get_all_readings_service
from app.core.utils import token_required

blood_sugar_bp = Blueprint('blood_sugar', __name__)

@blood_sugar_bp.route('/', methods=['POST'])
@token_required
def add_reading_route(current_user):
    """
    Endpoint untuk menambahkan data pembacaan gula darah baru.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body harus dalam format JSON."}), 400

    # ==============================================================
    #           PERBAIKAN 1: Siapkan 3 variabel untuk menerima 3 nilai
    # ==============================================================
    success, result, status_code = add_blood_sugar_service(current_user, data)

    if not success:
        return jsonify(result), status_code

    # ==============================================================
    #           PERBAIKAN 2: Kembalikan hasil dan status code yang benar
    # ==============================================================
    return jsonify(result), status_code


@blood_sugar_bp.route('/', methods=['GET'])
@token_required
def get_readings_route(current_user):
    """
    Endpoint untuk mengambil semua riwayat pembacaan gula darah.
    """
    # Mengikuti pola yang sama untuk konsistensi
    readings, error_message, status_code = get_all_readings_service(current_user)

    if error_message:
        return jsonify({"message": error_message}), status_code

    return jsonify(readings), status_code