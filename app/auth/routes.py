from flask import Blueprint, request, jsonify
from app.auth import services

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint untuk mendaftarkan user baru."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body harus dalam format JSON."}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"message": "Username, email, dan password wajib diisi."}), 400

    response_data, message, status_code = services.register_user(username, email, password)

    if status_code >= 400:
        return jsonify({"status": "error", "message": message}), status_code
    
    return jsonify(response_data), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint untuk login user menggunakan username."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body harus dalam format JSON."}), 400

    # PERUBAHAN DI SINI: Mengambil 'username' dari request
    username = data.get('username')
    password = data.get('password')

    # PERUBAHAN DI SINI: Validasi input 'username'
    if not all([username, password]):
        return jsonify({"message": "Username dan password wajib diisi."}), 400
    
    # PERUBAHAN DI SINI: Memanggil service dengan 'username'
    response_data, message, status_code = services.login_user(username, password)

    if status_code >= 400:
        return jsonify({"status": "error", "message": message}), status_code

    return jsonify(response_data), status_code
