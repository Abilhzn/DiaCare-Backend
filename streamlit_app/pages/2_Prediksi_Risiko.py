# streamlit_app/pages/2_Prediksi_Risiko.py

import streamlit as st
import requests
from config import BACKEND_URL

st.set_page_config(page_title="Prediksi Risiko Diabetes", page_icon="🔮", layout="centered")

def get_auth_header():
    token = st.session_state.get('auth_token')
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}

if not st.session_state.get('auth_token'):
    st.warning("Anda harus masuk terlebih dahulu untuk mengakses halaman ini.")
    st.markdown("Silakan kembali ke halaman **[Home](/)** untuk login.")
    st.stop()

st.title("🔮 Prediksi Risiko Diabetes")

with st.form("prediction_form"):
    st.write("Masukkan data kesehatan Anda selengkap mungkin untuk hasil prediksi yang lebih akurat:")
    
    col1, col2 = st.columns(2)
    with col1:
        # --- FITUR BARU ---
        gender = st.selectbox("Jenis Kelamin", ("Pria", "Wanita"))
        age = st.number_input("Usia", min_value=1, max_value=120, value=30)
        # --- FITUR BARU ---
        hypertension = st.selectbox("Memiliki Riwayat Hipertensi?", ("Tidak", "Ya"))
        weight = st.number_input("Berat Badan (kg)", min_value=10.0, value=70.0, format="%.1f")
        
    with col2:
        # --- FITUR BARU ---
        HbA1c_level = st.number_input("Kadar HbA1c (%)", min_value=4.0, max_value=16.0, value=5.7, step=0.1, format="%.1f")
        blood_glucose_level = st.number_input("Kadar Gula Darah Terakhir (mg/dL)", min_value=40, max_value=600, value=90)
        height = st.number_input("Tinggi Badan (cm)", min_value=50.0, value=170.0, format="%.1f")

    submitted = st.form_submit_button("Dapatkan Prediksi", use_container_width=True, type="primary")

    if submitted:
        headers = get_auth_header()
        if headers:
            # === Kirim semua data baru ke backend ===
            payload = {
                "gender": gender,
                "age": age,
                "hypertension": True if hypertension == "Ya" else False,
                "weight": weight,
                "height": height,
                "HbA1c_level": HbA1c_level,
                "blood_glucose_level": blood_glucose_level
            }
            with st.spinner("Menganalisis data dan membuat prediksi..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/diabetes/predict", headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        prediction_data = response.json()
                        risk_level = prediction_data.get("risk_level")
                        recommendation = prediction_data.get("recommendation")

                        st.divider()
                        st.subheader("✔️ Hasil Analisis Anda")

                        if risk_level == "Beresiko terkena Diabetes":
                            st.metric(label="Tingkat Risiko Diabetes", value=risk_level, delta="Waspada", delta_color="inverse")
                        else:
                            st.metric(label="Tingkat Risiko Diabetes", value=risk_level, delta="Bagus", delta_color="off")
                        
                        if recommendation:
                            st.info(f"💡 Rekomendasi Personal Untuk Anda: {recommendation.get('message', ' ')}")

                    else:
                        st.error(f"Gagal mendapatkan prediksi: {response.json().get('message', 'Error tidak diketahui')}")

                except requests.exceptions.ConnectionError:
                    st.error("Gagal terhubung ke server backend.")