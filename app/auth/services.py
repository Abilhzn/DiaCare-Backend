import re
from datetime import datetime
# from app import db
from app.auth.models import User, Profile
from app.models.base import db
from app.core.utils import encode_auth_token

# Validasi Email
def is_valid_gmail(email):
    return email.endswith("@gmail.com")

# Validasi Password
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

def register_user(username, email, password, full_name):
    """
    Mendaftarkan user baru, lengkap dengan profil awal.
    Mengembalikan tuple: (success: bool, response: dict)
    """

    # Cek apakah username atau email sudah ada
    if User.query.filter((User.username == username) | (User.email == email)).first():
        response = {"status": "error", "message": "Username atau Email sudah ada yang menggunakan."}
        return False, response
    
    try:
        # Buat objek User baru
        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)

        # Buat objek Profile baru dan isi dengan nama lengkap
        new_profile = Profile(full_name=full_name)

        # Hubungkan profil dengan user
        new_user.profile = new_profile
        
        # Simpan keduanya ke database
        db.session.add(new_user)
        db.session.commit()

        # Buat token
        auth_token = encode_auth_token(new_user.id)

        response = {
            "status": "success",
            "message": "Registrasi berhasil!",
            "auth_token": auth_token
        }
        return True, response

    except Exception as e:
        db.session.rollback()
        response = {"status": "error", "message": f"Terjadi kesalahan internal saat menyimpan data: {str(e)}"}
        return False, response

def authenticate_user(username, password):
    """Mengautentikasi user."""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user, "Login successful", 200
    return None, "Invalid username or password", 401 # Unauthorized

def create_or_update_profile(user_id, full_name=None, date_of_birth_str=None, height=None, weight=None, precondition=None, is_update=False):
    """Membuat atau memperbarui profil user."""
    user = User.query.get(user_id)
    if not user:
        return None, "User not found", 404

    profile = user.profile
    if not profile:
        if is_update: # Tidak bisa update jika profil belum ada
             return None, "Profile not found for this user. Create one first.", 404
        # Buat profil baru jika belum ada
        if not all([full_name, date_of_birth_str, height is not None, weight is not None, precondition is not None]):
            return None, "Missing required profile fields for creation.", 400
        profile = Profile(user_id=user_id)
        user.profile = profile # Associate profile with user
        db.session.add(profile) # Add to session if new
    
    # Update fields jika ada nilainya
    if full_name is not None:
        profile.full_name = full_name
    
    if date_of_birth_str is not None:
        try:
            profile.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        except ValueError:
            return None, "Invalid date format. Please use YYYY-MM-DD.", 400
            
    if height is not None:
        try:
            profile.height = float(height)
        except ValueError:
            return None, "Invalid height format. Must be a number.", 400
            
    if weight is not None:
        try:
            profile.weight = float(weight)
        except ValueError:
            return None, "Invalid weight format. Must be a number.", 400

    if precondition is not None:
        if precondition not in ['iya', 'tidak', 'prediabetic']:
            return None, "Invalid precondition value. Allowed: 'iya', 'tidak', 'prediabetic'.", 400
        profile.precondition = precondition
    
    try:
        db.session.commit()
        action = "updated" if is_update or (profile.id and not all([full_name, date_of_birth_str, height, weight, precondition])) else "created"
        return profile, f"Profile {action} successfully", 200 if action == "updated" else 201
    except Exception as e:
        db.session.rollback()
        return None, f"Failed to save profile: {str(e)}", 500

def get_user_profile(user_id):
    """Mengambil profil user."""
    user = User.query.get(user_id)
    if not user:
        return None, "User not found", 404
    if not user.profile:
        return None, "Profile not found for this user. Please complete your profile.", 404 # Atau 200 dengan data kosong jika diinginkan
    
    # Informasi umur akan dihitung secara otomatis oleh property 'age' di model Profile
    return user.profile, "Profile retrieved successfully", 200

def login_user(email, password):
    """
    Melakukan login user dan mengecek status kelengkapan profil.
    Mengembalikan tuple: (success: bool, response: dict)
    """
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        user_status = "existing_user"
        if user.profile and not user.profile.is_complete:
            user_status = "new_user_profile_incomplete"
            
        auth_token = encode_auth_token(user.id)
        response_data = {
            'status': 'success',
            'message': 'Login berhasil.',
            'auth_token': auth_token,
            'user_status': user_status,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile': user.profile.to_dict() if user.profile else None 
            }
        }
        return True, response_data
    else:
        return False, {"status": "error", "message": "Email atau password salah."}