from app.models.base import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relasi one-to-one dengan Profile
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete-orphan")
    
    # Relasi one-to-many dengan pembacaan gula darah
    blood_sugar_readings = db.relationship('BloodSugarReading', backref='owner', lazy=True, cascade="all, delete-orphan")
    
    # Relasi one-to-many dengan notifikasi
    notifications = db.relationship('Notification', backref='recipient', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password  # Menggunakan setter

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    height = db.Column(db.Float, nullable=True) # dalam cm
    weight = db.Column(db.Float, nullable=True) # dalam kg
    precondition = db.Column(db.String(120), nullable=True)

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def to_dict(self):
        """Mengubah objek Profile menjadi format dictionary."""
        return {
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'precondition': self.precondition
        }

    def __repr__(self):
        return f'<Profile for User ID {self.user_id}>'
