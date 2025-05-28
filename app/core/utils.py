import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app, request, jsonify
from functools import wraps
from app.auth.models import User # Sesuaikan path jika User model ada di tempat lain

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=1, seconds=5), # Token berlaku 1 hari
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('JWT_SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

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
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify(message='Bearer token malformed.'), 401

        if not token:
            return jsonify(message='Token is missing!'), 401

        user_id_or_error = decode_auth_token(token)
        if isinstance(user_id_or_error, str): # Error message
            return jsonify(message=user_id_or_error), 401

        current_user = User.query.get(user_id_or_error)
        if not current_user:
            return jsonify(message='User not found.'), 401
        
        return f(current_user, *args, **kwargs)
    return decorated