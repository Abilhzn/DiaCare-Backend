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


def predict_diabetes_service(user, data): # Sesuai SC006 [cite: 12]
    model = load_model()
    
    # Validasi kelengkapan data (SC007) [cite: 12]
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

import joblib
from flask import current_app
import numpy as np # Biasanya dibutuhkan untuk preprosesing model ML
from app.models.base import db
from app.models.diabetes_prediction_result import DiabetesPredictionResult

# DUMMY MODEL - GANTI DENGAN MODEL ASLI ANDA
class DummyModel:
    def predict(self, features):
        # Contoh logika dummy berdasarkan gula darah dan usia
        # Features: [usia, berat_badan, gula_darah, tekanan_darah, riwayat_keluarga_bool]
        # Sesuai SC009 & SC010 [cite: 12]
        if len(features[0]) < 5: # Asumsi 5 fitur dasar
             raise ValueError("Data tidak lengkap untuk prediksi dummy.")
        gula_darah = features[0][2] 
        usia = features[0][0]

        if gula_darah > 150 and usia > 45: # Sesuai SC009 [cite: 12]
            return ["Tinggi"] 
        elif gula_darah < 100 and usia < 30: # Sesuai SC010 [cite: 12]
            return ["Rendah"]
        else:
            return ["Sedang"]

    def predict_proba(self, features):
        # Dummy probabilities
        gula_darah = features[0][2]
        usia = features[0][0]
        if gula_darah > 150 and usia > 45:
            return np.array([[0.1, 0.2, 0.7]]) # Rendah, Sedang, Tinggi
        elif gula_darah < 100 and usia < 30:
            return np.array([[0.7, 0.2, 0.1]])
        else:
            return np.array([[0.3, 0.5, 0.2]])

def load_model():
    model_path = current_app.config['MODEL_PATH']
    try:
        # model = joblib.load(model_path)
        # Karena kita belum punya model.pkl, kita pakai dummy
        print(f"INFO: Menggunakan DUMMY MODEL. Ganti dengan model asli di: {model_path}")
        model = DummyModel() 
        return model
    except FileNotFoundError:
        print(f"ERROR: File model tidak ditemukan di {model_path}. Menggunakan DUMMY MODEL.")
        return DummyModel() # Fallback ke dummy jika file tidak ada
    except Exception as e:
        print(f"ERROR: Gagal memuat model: {e}. Menggunakan DUMMY MODEL.")
        return DummyModel()


def predict_diabetes_service(user, data): # Sesuai SC006 [cite: 12]
    model = load_model()
    
    # Validasi kelengkapan data (SC007) [cite: 12]
    required_fields = ['age', 'weight', 'blood_glucose_level', 'blood_pressure', 'family_history']
    for field in required_fields:
        if field not in data or data[field] is None:
            return None, f"Harap lengkapi semua data. Field '{field}' tidak boleh kosong."

    # Validasi tipe data numerik (SC008) [cite: 12]
    numeric_fields = ['age', 'weight', 'blood_glucose_level', 'blood_pressure']
    for field in numeric_fields:
        try:
            data[field] = float(data[field])
        except (ValueError, TypeError):
            return None, f"Field '{field}' harus berupa angka yang valid."

    try:
        # Sesuaikan urutan dan jenis fitur dengan yang diharapkan model Anda
        # Contoh: [usia, berat_badan, gula_darah, tekanan_darah, riwayat_keluarga_bool]
        # Pastikan data 'family_history' dikonversi ke format yang sesuai (misal, 0 atau 1)
        family_history_bool = True if str(data.get('family_history', 'false')).lower() == 'true' else False
        
        features = np.array([[
            data['age'], 
            data['weight'], 
            data['blood_glucose_level'], 
            data['blood_pressure'],
            1 if family_history_bool else 0 # Contoh konversi ke numerik jika model butuh
        ]])
        
        # Misalkan model.predict() mengembalikan array seperti ['Tinggi']
        prediction_raw = model.predict(features)
        prediction_label = prediction_raw[0] # Ambil label stringnya

        # Simpan hasil prediksi ke database
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
    except ValueError as ve: # Untuk handle error dari dummy model jika data tidak lengkap
        return None, str(ve)
    except Exception as e:
        current_app.logger.error(f"Error saat prediksi: {e}")
        return None, "Terjadi kesalahan saat melakukan prediksi."