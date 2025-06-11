# app/models/blood_sugar_reading.py

from .base import db
from datetime import datetime

class BloodSugarReading(db.Model):
    """
    Model untuk menyimpan setiap catatan kadar gula darah pengguna.
    """
    __tablename__ = 'blood_sugar_readings'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True) # Catatan tambahan, boleh kosong
    condition = db.Column(db.String(50), nullable=True) # Misal: 'sebelum_makan', 'setelah_makan', 'sebelum_tidur'

    # --- Kunci Hubungan Antar Tabel ---
    # Kolom ini adalah Foreign Key yang menghubungkan setiap catatan
    # ke seorang pengguna di tabel 'users'.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """
        Representasi string dari objek untuk mempermudah debugging.
        """
        return f'<BloodSugarReading {self.id} (User {self.user_id}) - {self.value} mg/dL>'

    def to_dict(self):
        """
        Mengubah objek model ini menjadi format dictionary agar mudah diubah ke JSON.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'value': self.value,
            'timestamp': self.timestamp.isoformat() + 'Z', # Format ISO 8601 yang umum untuk API
            'notes': self.notes,
            'condition': self.condition
        }