import joblib
import os
from flask import current_app
import numpy as np
from app.models.base import db
from app.models.diabetes_prediction_result import DiabetesPredictionResult
from app.recommendations.services import get_recommendation_service
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd

def load_model():
    # model_path = current_app.config.get('MODEL_PATH', 'ml_model/diabtes_predict_model.pkl')
    model_path = 'app/diabetes_prediction/ml_model/diabtes_predict_model.pkl'
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

def calculate_bmi(weight, height):
    """Menghitung BMI dari berat (kg) dan tinggi (cm)."""
    if height is None or weight is None or height == 0:
        return 0
    return weight / ((height / 100) ** 2)

def predict_diabetes_service(user, prediction_data):
    """
    Melakukan prediksi risiko diabetes dan memanggil service rekomendasi
    dengan fitur-fitur yang sudah diupdate.
    """
    try:
        # Muat model
        model = load_model()

        # --- Ekstrak semua data yang dibutuhkan dari payload ---
        gender = prediction_data.get('gender')
        age = prediction_data.get('age')
        hypertension_bool = prediction_data.get('hypertension')
        weight = prediction_data.get('weight')
        height = prediction_data.get('height')
        glucose = prediction_data.get('blood_glucose_level')
        hba1c = prediction_data.get('HbA1c_level')
        
        # Validasi input dasar
        if not all([gender, age, hypertension_bool is not None, weight, height, hba1c, glucose]):
            return None, None, "Data input tidak lengkap. Semua field wajib diisi.", 400

        hypertension = 1 if hypertension_bool else 0
        
        bmi = calculate_bmi(weight, height)

        features = np.array([[
            gender, 
            age, 
            hypertension, 
            bmi, 
            glucose,
            hba1c
        ]])

        # Buat DataFrame dari features untuk preprocessing
        feature_names = ['gender', 'age', 'hypertension', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        df_features = pd.DataFrame(features, columns=feature_names)
        
        # Lakukan prediksi
        prediction_result = model.predict(df_features)
        
        # Mapping hasil prediksi ke teks
        risk_map = {0: "Tidak beresiko terkena Diabetes", 1: "Beresiko terkena Diabetes"}
        risk_level = risk_map.get(prediction_result[0], "Tidak Diketahui")

        # Panggil service rekomendasi yang sudah ada
        cat = "sehat"
        if prediction_result == 1 : cat = "diabetes"
        recommendation_text = get_recommendation_service(
            age,
            glucose,
            'sebelum',
            cat
        )

        return risk_level, recommendation_text, None, 200

    except FileNotFoundError:
        return None, None, "File model prediksi tidak ditemukan.", 500
    except Exception as e:
        return None, None, f"Terjadi kesalahan saat prediksi: {str(e)}", 500