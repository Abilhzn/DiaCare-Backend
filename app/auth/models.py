from app.models.base import db # Mengambil objek SQLAlchemy utama
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

class User(db.Model):
    tablename = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Membuat hubungan satu-ke-satu dengan Profile
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def repr(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    tablename = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    precondition = db.Column(db.String(50), nullable=True) # Misal: 'sehat', 'pradiabetes', 'diabetes'
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Foreign Key yang menghubungkan ke tabel 'users'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    @property
    def age(self):
        """Menghitung umur secara dinamis dari tanggal lahir."""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @property
    def is_complete(self):
        """Mengecek apakah profil sudah diisi dengan data esensial."""
        # Kita anggap lengkap jika nama & tanggal lahir sudah diisi
        if self.full_name and self.date_of_birth:
            return True
        return False

    def to_dict(self):
        """Mengubah objek profil menjadi dictionary."""
        return {
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'precondition': self.precondition
        }

    def repr(self):
        return f'<Profile for User ID {self.user_id}>'