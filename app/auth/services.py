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

def create_user(username, email, password):
    """Membuat user baru."""
    if User.query.filter_by(username=username).first():
        return None, "Username already exists", 409 # Conflict
    if User.query.filter_by(email=email).first():
        return None, "Email already exists", 409

    if not is_valid_gmail(email):
        return None, "Invalid email format. Must be a @gmail.com address.", 400 # Bad Request
    
    if not is_valid_password(password):
        return None, "Password must be at least 8 characters long and include uppercase, lowercase, and a number.", 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user, "User created successfully", 201 # Created
    except Exception as e:
        db.session.rollback()
        return None, f"Failed to create user: {str(e)}", 500 # Internal Server Error

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
    """
    try:
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Login berhasil, sekarang cek profilnya
            
            user_status = "existing_user" # Asumsi default pengguna lama
            
            # Cek apakah profil sudah lengkap menggunakan property yang kita buat
            if user.profile and not user.profile.is_complete:
                user_status = "new_user_profile_incomplete"
            
            auth_token = encode_auth_token(user.id)
            
            response_data = {
                'status': 'success',
                'message': 'Login berhasil.',
                'auth_token': auth_token,
                'user_status': user_status, # <-- KIRIM STATUS INI KE FRONTEND
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    # Kirim juga data profil jika ada
                    'profile': user.profile.to_dict() if user.profile else None 
                }
            }
            return response_data
            
        else:
            return None # Kembalikan None jika login gagal

    except Exception as e:
        # Sebaiknya log error di sini
        return None