from app.auth.services import create_user, login_user
from app.core.utils import encode_auth_token
from flask import Blueprint, request, jsonify
from app.auth import services
from app.auth.models import User, Profile
from app.models.base import db
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

    # Validasi input dasar bisa ditambahkan di sini
    if not all([username, email, password]):
        return jsonify({"error": "Missing username, email, or password"}), 400

    user, error_message, status_code = services.create_user(username, email, password)
    if error_message:
        return jsonify({"error": error_message}), status_code
    
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

    
    return jsonify({"message": "Login successful", "user_id": user.id}), 200 

def create_user(username, email, password, full_name):
    """
    Mendaftarkan user baru, lengkap dengan profil awal.
    """
    # Cek apakah username atau email sudah ada
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return False, {"status": "error", "message": "Username atau Email sudah ada yang menggunakan."}

    try:
        # Buat objek User baru
        new_user = User(
            username=username,
            email=email,
            password=password # Password akan di-hash di dalam model User
        )

        # Buat objek Profile baru dan isi dengan nama lengkap
        new_profile = Profile(
            full_name=full_name
            # Field lain (height, weight, dll) akan kosong (None)
        )

        # Hubungkan profil dengan user
        new_user.profile = new_profile
        
        # Simpan keduanya ke database
        db.session.add(new_user)
        # db.session.add(new_profile) # Tidak perlu di-add lagi karena sudah terhubung via relationship
        db.session.commit()

        # Buat token agar bisa langsung login jika diinginkan (opsional)
        auth_token = encode_auth_token(new_user.id)

        response_data = {
            "status": "success",
            "message": "Registrasi berhasil!",
            "auth_token": auth_token
        }
        return True, response_data

    except Exception as e:
        # Jika terjadi error lain saat menyimpan ke database
        db.session.rollback() # Batalkan transaksi jika ada error
        return False, {"status": "error", "message": str(e)}


@auth_bp.route('/profile', methods=['POST', 'GET', 'PUT'])
# @login_required # Jika menggunakan Flask-Login
# @jwt_required() # Jika menggunakan Flask-JWT-Extended
def profile_management():
    user_id = request.headers.get('X-User-Id') # Contoh, atau ambil dari token JWT
    if not user_id:
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