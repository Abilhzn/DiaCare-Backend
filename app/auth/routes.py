from flask import Blueprint, request, jsonify
from app.auth import services
from app.auth.models import User # Mungkin diperlukan untuk type hinting atau query langsung jika services tidak mencakup semua
# Jika Anda menggunakan Flask-Login atau Flask-JWT-Extended untuk manajemen sesi/token
# from flask_login import login_user, logout_user, login_required, current_user
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validasi input dasar bisa ditambahkan di sini atau di services
    if not all([username, email, password]):
        return jsonify({"error": "Missing username, email, or password"}), 400

    user, error_message, status_code = services.create_user(username, email, password)
    if error_message:
        return jsonify({"error": error_message}), status_code
    
    # Setelah sign up, Anda bisa langsung meminta data profil atau membuat endpoint terpisah
    # Di sini, kita asumsikan user akan mengisi profil setelah login atau di langkah berikutnya
    return jsonify({"message": "User created successfully. Please complete your profile.", "user_id": user.id}), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Missing username or password"}), 400

    user, error_message, status_code = services.authenticate_user(username, password)
    if error_message:
        return jsonify({"error": error_message}), status_code

    # Jika menggunakan Flask-Login:
    # login_user(user)
    
    # Jika menggunakan Flask-JWT-Extended:
    # access_token = create_access_token(identity=user.id)
    # return jsonify(access_token=access_token, message="Login successful"), 200
    
    return jsonify({"message": "Login successful", "user_id": user.id}), 200 # Sesuaikan respons sesuai kebutuhan

@auth_bp.route('/profile', methods=['POST', 'GET', 'PUT'])
# @login_required # Jika menggunakan Flask-Login
# @jwt_required() # Jika menggunakan Flask-JWT-Extended
def profile_management():
    # user_id = current_user.id # Jika menggunakan Flask-Login
    # user_id = get_jwt_identity() # Jika menggunakan Flask-JWT-Extended
    
    # Untuk sementara, kita akan mengambil user_id dari request header atau body
    # Ini HANYA untuk contoh, idealnya gunakan sistem autentikasi yang proper
    user_id = request.headers.get('X-User-Id') # Contoh, atau ambil dari token JWT
    if not user_id:
        # Coba ambil dari body jika POST atau PUT dan tidak di header
        if request.method in ['POST', 'PUT']:
            data = request.get_json()
            user_id = data.get('user_id') if data else None
        
        if not user_id:
            return jsonify({"error": "User not authenticated or user_id missing"}), 401
    
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user_id format"}), 400


    if request.method == 'POST': # Membuat profil (setelah sign up jika belum ada)
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        full_name = data.get('full_name')
        date_of_birth_str = data.get('date_of_birth') # Format YYYY-MM-DD
        height = data.get('height')
        weight = data.get('weight')
        precondition = data.get('precondition')

        if not all([full_name, date_of_birth_str, height is not None, weight is not None, precondition]):
             return jsonify({"error": "Missing profile data: full_name, date_of_birth, height, weight, precondition are required."}), 400

        profile, error_message, status_code = services.create_or_update_profile(
            user_id=user_id,
            full_name=full_name,
            date_of_birth_str=date_of_birth_str,
            height=height,
            weight=weight,
            precondition=precondition
        )
        if error_message:
            return jsonify({"error": error_message}), status_code
        return jsonify({"message": "Profile created successfully", "profile_id": profile.id}), status_code

    elif request.method == 'GET':
        profile, error_message, status_code = services.get_user_profile(user_id)
        if error_message:
            return jsonify({"error": error_message}), status_code
        
        return jsonify({
            "user_id": profile.user_id,
            "full_name": profile.full_name,
            "date_of_birth": profile.date_of_birth.isoformat() if profile.date_of_birth else None,
            "age": profile.age,
            "height": profile.height,
            "weight": profile.weight,
            "precondition": profile.precondition
        }), status_code

    elif request.method == 'PUT': # Memperbarui profil
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        profile, error_message, status_code = services.create_or_update_profile(
            user_id=user_id,
            full_name=data.get('full_name'),
            date_of_birth_str=data.get('date_of_birth'), # Format YYYY-MM-DD
            height=data.get('height'),
            weight=data.get('weight'),
            precondition=data.get('precondition'),
            is_update=True
        )
        if error_message:
            return jsonify({"error": error_message}), status_code
        return jsonify({"message": "Profile updated successfully", "profile_id": profile.id}), status_code
    
    return jsonify({"error": "Method not allowed"}), 405