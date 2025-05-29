from app.models.base import db
from datetime import datetime, timezone

class DiabetesPredictionResult(db.Model):
    __tablename__ = 'diabetes_prediction_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Simpan input yang digunakan untuk prediksi
    age = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True) # Asumsi ada field berat badan
    blood_glucose_level = db.Column(db.Float, nullable=True) # Asumsi field gula darah
    blood_pressure = db.Column(db.Float, nullable=True) # Asumsi field tekanan darah
    family_history = db.Column(db.Boolean, nullable=True) # Asumsi field riwayat keluarga
    # ... tambahkan field input lain sesuai model
    
    prediction_result = db.Column(db.String(50), nullable=False) # Misal: "Rendah", "Sedang", "Tinggi"
    predicted_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<DiabetesPredictionResult {self.user_id} - {self.prediction_result}>'