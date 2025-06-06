import joblib
from flask import current_app
import numpy as np
from app.models.base import db
from app.models.diabetes_prediction_result import DiabetesPredictionResult

def load_model():
    model_path = current_app.config.get('MODEL_PATH', 'ml_model/diabetes_predict_dataset.pkl')
    try:
        model = joblib.load(model_path)
        print(f"INFO: Model berhasil dimuat dari {model_path}")
        return model
    except FileNotFoundError:
        print(f"ERROR: File model tidak ditemukan di {model_path}.")
        raise
    except Exception as e:
        print(f"ERROR: Gagal memuat model: {e}.")
        raise

def predict_diabetes_service(user, data):
    try:
        model = load_model()
    except Exception as e:
        return None, f"Gagal memuat model: {e}"

    required_fields = ['age', 'weight', 'blood_glucose_level', 'blood_pressure', 'family_history']
    for field in required_fields:
        if field not in data or data[field] is None:
            return None, f"Harap lengkapi semua data. Field '{field}' tidak boleh kosong."

    numeric_fields = ['age', 'weight', 'blood_glucose_level', 'blood_pressure']
    for field in numeric_fields:
        try:
            data[field] = float(data[field])
        except (ValueError, TypeError):
            return None, f"Field '{field}' harus berupa angka yang valid."

    try:
        family_history_bool = True if str(data.get('family_history', 'false')).lower() == 'true' else False

        # Pastikan urutan fitur sesuai dengan model asli
        features = np.array([[
            data['age'],
            data['weight'],
            data['blood_glucose_level'],
            data['blood_pressure'],
            1 if family_history_bool else 0
        ]])

        prediction_raw = model.predict(features)
        prediction_label = prediction_raw[0]

        prediction_entry = DiabetesPredictionResult(
            user_id=user.id,
            age=data['age'],
            weight=data['weight'],
            blood_glucose_level=data['blood_glucose_level'],
            blood_pressure=data['blood_pressure'],
            family_history=family_history_bool,
            prediction_result=prediction_label
        )
        db.session.add(prediction_entry)
        db.session.commit()

        return {"risk_level": prediction_label, "details": "Prediksi berhasil."}, None
    except Exception as e:
        current_app.logger.error(f"Error saat prediksi: {e}")
        return None, "Terjadi kesalahan saat melakukan prediksi."

