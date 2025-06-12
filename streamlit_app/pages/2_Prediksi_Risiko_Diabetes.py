import streamlit as st
import requests
import json

st.set_page_config(page_title="Prediksi Risiko", page_icon="🔮", layout="centered")

BACKEND_URL = "http://127.0.0.1:5000/api"

def get_auth_header():
    token = st.session_state.get('auth_token')
    if not token:
        return None
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

if 'auth_token' not in st.session_state or st.session_state.auth_token is None:
    st.warning("Anda harus masuk terlebih dahulu untuk mengakses halaman ini.")
    st.markdown("Silakan kembali ke halaman **[Home](/)** untuk login.")
    st.stop()

st.title("🔮 Prediksi Risiko Diabetes")

with st.form("prediction_form"):
    st.write("Masukkan data kesehatan Anda untuk prediksi:")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Usia", min_value=1, max_value=120, value=30)
        weight = st.number_input("Berat Badan (kg)", min_value=10.0, value=70.0, format="%.1f")
        height = st.number_input("Tinggi Badan (cm)", min_value=50.0, value=170.0, format="%.1f")
    with col2:
        glucose = st.number_input("Kadar Gula Darah Terakhir (mg/dL)", min_value=40, max_value=600, value=90)
        family_history = st.selectbox("Riwayat Keluarga Diabetes?", ("Tidak", "Ya"))

    if st.form_submit_button("Dapatkan Prediksi", use_container_width=True):
        headers = get_auth_header()
        if headers:
            payload = {
                "age": age,
                "weight": weight,
                "height": height,
                "blood_glucose_level": glucose,
                "family_history": True if family_history == "Ya" else False,
                # Tambahkan field lain jika modelmu butuh
            }
            try:
                response = requests.post(f"{BACKEND_URL}/diabetes/predict", headers=headers, json=payload)
                if response.status_code == 200:
                    prediction_data = response.json()
                    risk_level = prediction_data.get("risk_level")
                    st.metric(label="Hasil Prediksi Risiko Diabetes Anda", value=risk_level)
                    if risk_level == "Tinggi":
                        st.error("Risiko Anda TINGGI. Segera konsultasikan dengan dokter dan mulai pemantauan rutin.", icon="🚨")
                    elif risk_level == "Sedang":
                        st.warning("Risiko Anda SEDANG. Jaga pola hidup sehat dan lakukan pemeriksaan berkala.", icon="⚠️")
                    else:
                        st.success("Risiko Anda RENDAH. Tetap pertahankan gaya hidup sehat!", icon="✅")
                else:
                    st.error(f"Gagal mendapatkan prediksi: {response.json().get('message', 'Error tidak diketahui')}")
            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke server backend.")