import re
from app import db
from app.auth.models import User
# Pastikan Anda memiliki fungsi ini di app/core/utils.py
from app.core.utils import encode_auth_token 

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

def register_user(username, email, password):
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
        # Buat objek User baru
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Simpan ke database
        db.session.add(new_user)
        db.session.commit()

        # Buat token agar user bisa langsung login
        auth_token = encode_auth_token(new_user.id)

        response_data = {
            "status": "success",
            "auth_token": auth_token
        }
        return response_data, "Registrasi berhasil!", 201

    except Exception as e:
        db.session.rollback()
        return None, f"Terjadi kesalahan internal: {str(e)}", 500

def login_user(email, password):
    """
    Melakukan login user.
    Mengembalikan tuple: (data, message, status_code)
    """
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        auth_token = encode_auth_token(user.id)
        response_data = {
            'status': 'success',
            'auth_token': auth_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }
        return response_data, 'Login berhasil.', 200
    else:
        return None, "Email atau password salah.", 401
