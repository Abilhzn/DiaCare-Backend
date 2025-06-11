from flask import request, jsonify
from . import blood_sugar_bp
from .services import (
    add_blood_sugar_service,
    get_user_readings_service, # Nama fungsi diubah agar lebih jelas
    get_reading_by_id_service,
    update_reading_service,
    delete_reading_service
)
from app.core.utils import token_required

@blood_sugar_bp.route('', methods=['POST'])
@token_required
def add_reading_route(current_user):
    data = request.get_json()
    # Panggil service dan SERTAKAN current_user
    success, result = add_blood_sugar_service(current_user, data)
    if not success:
        return jsonify(message=result), 400
    return jsonify(result), 201

@blood_sugar_bp.route('', methods=['GET'])
@token_required
def get_all_readings_route(current_user):
    # Panggil service dan SERTAKAN current_user agar hanya data miliknya yang diambil
    readings = get_user_readings_service(current_user)
    return jsonify(readings), 200

@blood_sugar_bp.route('/<int:reading_id>', methods=['GET'])
@token_required
def get_single_reading_route(current_user, reading_id):
    # Sertakan current_user untuk validasi kepemilikan
    reading = get_reading_by_id_service(current_user, reading_id)
    if not reading:
        return jsonify(message="Data tidak ditemukan atau Anda tidak memiliki akses."), 404
    return jsonify(reading), 200

# Lakukan hal yang sama untuk PUT dan DELETE, sertakan current_user untuk otorisasi
@blood_sugar_bp.route('/<int:reading_id>', methods=['PUT'])
@token_required
def update_reading_route(current_user, reading_id):
    data = request.get_json()
    success, result = update_reading_service(current_user, reading_id, data)
    if not success:
        return jsonify(message=result), 404 # 404 jika not found/unauthorized
    return jsonify(message=result), 200

@blood_sugar_bp.route('/<int:reading_id>', methods=['DELETE'])
@token_required
def delete_reading_route(current_user, reading_id):
    success, message = delete_reading_service(current_user, reading_id)
    if not success:
        return jsonify(message=message), 404 # 404 jika not found/unauthorized
    return jsonify(message=message), 200from flask import request, jsonify
from . import blood_sugar_bp
from .services import (
    add_blood_sugar_service,
    get_user_readings_service,
    get_reading_by_id_service,
    update_reading_service,
    delete_reading_service
)
from app.core.utils import token_required

@blood_sugar_bp.route('', methods=['POST'])
@token_required
def add_reading_route(current_user):
    data = request.get_json()
    # Panggil service dan SERTAKAN current_user
    success, result = add_blood_sugar_service(current_user, data)
    if not success:
        return jsonify(message=result), 400
    return jsonify(result), 201

@blood_sugar_bp.route('', methods=['GET'])
@token_required
def get_all_readings_route(current_user):
    # Panggil service dan SERTAKAN current_user agar hanya data miliknya yang diambil
    readings = get_user_readings_service(current_user)
    return jsonify(readings), 200

@blood_sugar_bp.route('/<int:reading_id>', methods=['GET'])
@token_required
def get_single_reading_route(current_user, reading_id):
    # Sertakan current_user untuk validasi kepemilikan
    reading = get_reading_by_id_service(current_user, reading_id)
    if not reading:
        return jsonify(message="Data tidak ditemukan atau Anda tidak memiliki akses."), 404
    return jsonify(reading), 200

# Lakukan hal yang sama untuk PUT dan DELETE, sertakan current_user untuk otorisasi
@blood_sugar_bp.route('/<int:reading_id>', methods=['PUT'])
@token_required
def update_reading_route(current_user, reading_id):
    data = request.get_json()
    success, result = update_reading_service(current_user, reading_id, data)
    if not success:
        return jsonify(message=result), 404 # 404 jika not found/unauthorized
    return jsonify(message=result), 200

@blood_sugar_bp.route('/<int:reading_id>', methods=['DELETE'])
@token_required
def delete_reading_route(current_user, reading_id):
    success, message = delete_reading_service(current_user, reading_id)
    if not success:
        return jsonify(message=message), 404 # 404 jika not found/unauthorized
    return jsonify(message=message), 200