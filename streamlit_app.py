# # streamlit_app.py

# import streamlit as st
# import requests
# import json

# # URL base dari API backend Flask kamu
# BASE_URL = "http://127.0.0.1:5000/api"

# st.set_page_config(page_title="DiaCare", layout="centered")
# st.title("🩺 DiaCare - Aplikasi Deteksi & Pemantauan Diabetes")

# # --- Bagian Login & Registrasi ---
# st.header("1. Masuk atau Buat Akun")

# # Gunakan session state untuk menyimpan status login dan token
# if 'auth_token' not in st.session_state:
#     st.session_state.auth_token = None
# if 'user_name' not in st.session_state:
#     st.session_state.user_name = None

# if st.session_state.auth_token:
#     st.success(f"Anda masuk sebagai: **{st.session_state.user_name}**")
#     if st.button("Keluar"):
#         st.session_state.auth_token = None
#         st.session_state.user_name = None
#         st.rerun() # Muat ulang halaman
# else:
#     with st.form("login_form"):
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#         submitted = st.form_submit_button("Masuk")

#         if submitted:
#             try:
#                 response = requests.post(
#                     f"{BASE_URL}/auth/login",
#                     headers={"Content-Type": "application/json"},
#                     data=json.dumps({"email": email, "password": password})
#                 )
#                 if response.status_code == 200:
#                     data = response.json()
#                     st.session_state.auth_token = data.get("auth_token")
#                     st.session_state.user_name = data.get("user", {}).get("name")
#                     st.success("Login berhasil!")
#                     st.rerun() # Muat ulang halaman untuk update status
#                 else:
#                     st.error(f"Gagal login: {response.json().get('message', 'Error tidak diketahui')}")
#             except requests.exceptions.ConnectionError:
#                 st.error("Tidak dapat terhubung ke server backend. Pastikan backend sudah berjalan.")

# # --- Bagian Prediksi Diabetes (Hanya muncul jika sudah login) ---
# if st.session_state.auth_token:
#     st.header("2. Prediksi Risiko Diabetes")
    
#     with st.form("prediction_form"):
#         st.write("Masukkan data kesehatan Anda:")
        
#         # Buat kolom agar lebih rapi
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Usia", min_value=1, max_value=120, value=30)
#             weight = st.number_input("Berat Badan (kg)", min_value=10.0, value=70.0, format="%.1f")
#             height = st.number_input("Tinggi Badan (cm)", min_value=50.0, value=170.0, format="%.1f")
#         with col2:
#             glucose = st.number_input("Kadar Gula Darah (mg/dL)", min_value=40, max_value=600, value=90)
#             family_history = st.selectbox("Riwayat Keluarga Diabetes?", ("Tidak", "Ya"))

#         predict_button = st.form_submit_button("Dapatkan Prediksi")

#         if predict_button:
#             # Siapkan header dengan token otentikasi
#             headers = {
#                 "Authorization": f"Bearer {st.session_state.auth_token}",
#                 "Content-Type": "application/json"
#             }
#             # Siapkan data payload
#             payload = {
#                 "age": age,
#                 "weight": weight,
#                 "height": height, # Asumsi model butuh tinggi, atau bisa dihitung BMI dulu
#                 "blood_glucose_level": glucose, # Sesuaikan nama field dengan API-mu
#                 "family_history": True if family_history == "Ya" else False
#             }

#             try:
#                 response = requests.post(
#                     f"{BASE_URL}/diabetes/predict",
#                     headers=headers,
#                     data=json.dumps(payload)
#                 )

#                 if response.status_code == 200:
#                     prediction_data = response.json()
#                     risk_level = prediction_data.get("risk_level")
#                     st.metric(label="Hasil Prediksi Risiko Diabetes", value=risk_level)
#                     if risk_level == "Tinggi":
#                         st.warning("Risiko Anda TINGGI. Disarankan untuk segera berkonsultasi dengan dokter dan memulai pemantauan rutin.")
#                     elif risk_level == "Sedang":
#                         st.info("Risiko Anda SEDANG. Jaga pola hidup sehat dan lakukan pemeriksaan berkala.")
#                     else:
#                         st.success("Risiko Anda RENDAH. Tetap pertahankan gaya hidup sehat!")
#                 else:
#                     st.error(f"Gagal mendapatkan prediksi: {response.json().get('message', 'Error tidak diketahui')}")
#             except requests.exceptions.ConnectionError:
#                  st.error("Tidak dapat terhubung ke server backend.")

# # Kamu bisa menambahkan form dan logika untuk fitur lain di sini
# # seperti Pemantauan Gula Darah, melihat Rekomendasi, dll.