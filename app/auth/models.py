from app import db # Mengambil objek SQLAlchemy dari app/__init__.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """
    Model User yang sudah disederhanakan.
    Hanya berisi informasi dasar untuk login dan identifikasi.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Menghasilkan hash dari password dan menyimpannya."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Memverifikasi password dengan hash yang tersimpan."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
