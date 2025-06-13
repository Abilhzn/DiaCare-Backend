import re
from datetime import datetime
from app.models.base import db # <-- INI SOLUSINYA
from app.auth.models import User, Profile
from app.core.utils import encode_auth_token # Asumsi fungsi ini ada dan berfungsi

# --- Fungsi Helper untuk Validasi ---

def is_valid_gmail(email):
    """Memastikan email menggunakan domain @gmail.com."""
    if not isinstance(email, str):
        return False
    return email.lower().endswith("@gmail.com")

def is_valid_password(password):
    """
    Memastikan password memenuhi kriteria:
    - Minimal 8 karakter
    - Mengandung huruf kecil (a-z)
    - Mengandung huruf besar (A-Z)
    - Mengandung angka (0-9)
    """
    if not isinstance(password, str) or len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

# --- Service Functions ---

def register_user(username, email, password, full_name):
    """
    Mendaftarkan user baru dengan validasi ketat.
    Mengembalikan tuple: (data, message, status_code)
    """
    # 1. Validasi Email
    if not is_valid_gmail(email):
        return None, "Email harus menggunakan @gmail.com", 400

    # 2. Validasi Password
    if not is_valid_password(password):
        return None, "Password harus menggunakan huruf besar, huruf kecil, dan angka serta minimal 8 karakter", 400

    # 3. Cek apakah username atau email sudah ada
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return None, "Username atau Email sudah ada yang menggunakan.", 409

    try:
        new_user = User(
            username=username,
            email=email,
            password=password # <-- Argumen yang hilang sudah ditambahkan
        )

        # Buat objek Profile baru dan isi dengan nama lengkap
        new_profile = Profile(full_name=full_name)
        new_user.profile = new_profile

        # Simpan ke database
        db.session.add(new_user)
        db.session.commit()

        # Buat token
        auth_token = encode_auth_token(new_user.id)

        response_data = {
            "message": "Registrasi berhasil!",
            "user": { "id": new_user.id, "username": new_user.username },
            "auth_token": auth_token
        }
        return True, response_data, 201

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return None, f"Terjadi kesalahan internal: {str(e)}", 500

def login_user(email, password):
    """
    Memverifikasi kredensial dan mengembalikan data user lengkap beserta token.
    """
    try:
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            auth_token = encode_auth_token(user.id)
            
            # Ini adalah dictionary yang seharusnya dikirim
            response_data = {
                "status": "success",
                "message": "Login berhasil!",
                "auth_token": auth_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.profile.full_name if user.profile else user.username
                }
            }
            # Mengembalikan 3 nilai: True, dictionary data, dan kode 200
            return True, response_data, 200
        else:
            # Mengembalikan 3 nilai: False, dictionary error, dan kode 401
            return False, {"message": "Email atau password salah."}, 401

    except Exception as e:
        print(f"!!! LOGIN ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False, {"message": "Terjadi kesalahan pada server."}, 500

def get_user_profile(user_id):
    """
    Mengambil profil user.
    Mengembalikan tuple: (data, message, status_code)
    """
    user = User.query.get(user_id)
    if not user:
        return None, "User tidak ditemukan", 404
    if not user.profile:
        return None, "Profil belum dibuat untuk user ini.", 404
    
    return user.profile.to_dict(), "Profil berhasil diambil", 200

def create_or_update_profile(user_id, data, is_update=False):
    """
    Membuat atau memperbarui profil user.
    Mengembalikan tuple: (data, message, status_code)
    """
    user = User.query.get(user_id)
    if not user:
        return None, "User tidak ditemukan", 404

    profile = user.profile
    if not profile:
        if is_update:
             return None, "Profil tidak ditemukan, tidak bisa update.", 404
        profile = Profile(user_id=user_id)
        user.profile = profile

    # Update fields
    if 'full_name' in data:
        profile.full_name = data['full_name']
    if 'date_of_birth' in data:
        try:
            profile.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None, "Format tanggal lahir salah. Gunakan YYYY-MM-DD.", 400
    if 'height' in data:
        profile.height = data['height']
    if 'weight' in data:
        profile.weight = data['weight']
    if 'precondition' in data:
        if data['precondition'] not in ['iya', 'tidak', 'prediabetic']:
            return None, "Nilai precondition tidak valid. Pilih 'iya', 'tidak', atau 'prediabetic'.", 400
        profile.precondition = data['precondition']

    try:
        db.session.commit()
        message = "Profil berhasil diperbarui" if is_update else "Profil berhasil dibuat"
        return profile.to_dict(), message, 200 if is_update else 201
    except Exception as e:
        db.session.rollback()
        return None, f"Gagal menyimpan profil: {str(e)}", 500
