from flask import Blueprint, request, jsonify
from app.auth import services
# Ganti dengan mekanisme autentikasi Anda (misal: JWT) untuk mendapatkan user_id
# from flask_jwt_extended import jwt_required, get_jwt_identity 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body harus dalam format JSON."}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if not all([username, email, password, full_name]):
        return jsonify({"message": "Username, email, password, dan nama lengkap wajib diisi."}), 400

    # Panggil service untuk registrasi
    response_data, message, status_code = services.register_user(username, email, password, full_name)

    if status_code >= 400: # Jika ada error dari service

        return jsonify({"status": "error", "message": message}), status_code
    
    # Jika sukses
    return jsonify(response_data), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint untuk login user menggunakan username."""
    data = request.get_json()
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({"message": "Email dan password wajib diisi."}), 400


    # Panggil service dan siapkan 3 variabel untuk menampung hasilnya
    success, response_data, status_code = services.login_user(data['email'], data['password'])
    
    # KEMBALIKAN 'response_data' (yang berupa dictionary) SEBAGAI JSON
    # BUKAN 'success' (yang berupa boolean)
    return jsonify(response_data), status_code

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not all(k in data for k in ['email', 'password']):
#         return jsonify({"message": "Email dan password wajib diisi."}), 400
    
#     success, response_data, status_code = services.login_user(data['email'], data['password'])

#     email = data.get('email')
#     password = data.get('password')

#     if not all([email, password]):
#         return jsonify({"message": "Email dan password wajib diisi."}), 400
    
#     # Panggil service untuk login
#     response_data, message, status_code = services.login_user(email, password)

#     if status_code >= 400: # Jika login gagal
#         return jsonify({"status": "error", "message": message}), status_code

#     # Jika sukses
#     return jsonify(response_data), status_code

@auth_bp.route('/profile', methods=['GET', 'PUT'])
# @jwt_required() # Lindungi endpoint ini
def profile_management():
    # user_id = get_jwt_identity() # Cara yang benar untuk mendapatkan user_id dari token
    # Untuk sementara, kita pakai header (TIDAK AMAN UNTUK PRODUKSI)
    try:
        user_id = int(request.headers.get('X-User-Id'))
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "User ID tidak valid atau hilang dari header."}), 401
    
    if request.method == 'GET':
        response_data, message, status_code = services.get_user_profile(user_id)
        if status_code >= 400:
            return jsonify({"status": "error", "message": message}), status_code
        return jsonify(response_data), status_code

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Request body harus dalam format JSON."}), 400
        
        response_data, message, status_code = services.create_or_update_profile(user_id=user_id, data=data, is_update=True)
        if status_code >= 400:
            return jsonify({"status": "error", "message": message}), status_code
        
        response_data['message'] = message # Tambahkan pesan sukses ke respons
        return jsonify(response_data), status_code