import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app, request, jsonify
from functools import wraps
from app.core import config
from app.auth.models import User

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=1, seconds=5), # Token berlaku 1 hari
            'iat': datetime.now(timezone.utc),
            'sub': str(user_id)
        }

        secret_key = current_app.config.get('SECRET_KEY')
        print("--- [ENCODE] MEMBUAT TOKEN ---")
        print(f"--- [ENCODE] SECRET KEY: {secret_key}")
        print(f"--- [ENCODE] PAYLOAD: {payload}")

        token = jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )

        return token
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('JWT_SECRET_KEY'), algorithms=['HS256'])
        return payload['sub'] # user_id
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(f):
    """
    Decorator untuk memastikan endpoint memerlukan token yang valid.
    Setelah verifikasi, akan mengambil objek User dari database.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Format token tidak benar.'}), 401

        if not token:
            return jsonify({'message': 'Token tidak ditemukan!'}), 401

        try:
            secret_key = current_app.config.get('SECRET_KEY')
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            
            
            user_id_from_token = data['sub']
            # Cari user di database berdasarkan ID dari token
            current_user = User.query.get(user_id_from_token) 
            
            # Pengaman jika user-nya ternyata sudah dihapus dari DB
            if not current_user:
                return jsonify({'message': 'User dengan token ini tidak ditemukan!'}), 404
            

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token sudah kedaluwarsa!'}), 401
        except jwt.InvalidTokenError:
            # Ini seharusnya tidak terjadi lagi, tapi untuk jaga-jaga
            return jsonify({'message': 'Token tidak valid. Silakan login kembali.'}), 401

        # Teruskan OBJEK USER LENGKAP, bukan cuma ID-nya
        return f(current_user, *args, **kwargs) 

    return decorated