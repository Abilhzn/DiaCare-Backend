import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Pemantauan Gula Darah", page_icon="🩸", layout="wide")

BACKEND_URL = "http://127.0.0.1:5000/api"

# --- FUNGSI BANTUAN ---
def get_auth_header():
    token = st.session_state.get('auth_token')
    if not token:
        return None
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# --- KUNCI: Cek status login di setiap halaman ---
if 'auth_token' not in st.session_state or st.session_state.auth_token is None:
    st.warning("Anda harus masuk terlebih dahulu untuk mengakses halaman ini.")
    st.markdown("Silakan kembali ke halaman **[Home](/)** untuk login.")
    st.stop() # Hentikan eksekusi script jika belum login

# --- TAMPILAN HALAMAN ---
st.title("🩸 Catat dan Pantau Gula Darah")

col1, col2 = st.columns([1, 2]) # Buat kolom agar lebih rapi, kolom kedua lebih lebar

with col1:
    st.subheader("Input Data Baru")
    with st.form("reading_form"):
        glucose_value = st.number_input("Kadar Gula Darah (mg/dL)", min_value=20, max_value=600, value=100)
        condition = st.selectbox("Kondisi Pengukuran", ["sebelum_makan", "setelah_makan", "sebelum_tidur"])
        notes = st.text_area("Catatan (opsional)")
        
        if st.form_submit_button("Simpan Data", use_container_width=True):
            headers = get_auth_header()
            if headers:
                payload = {"value": glucose_value, "condition": condition, "notes": notes}
                try:
                    response = requests.post(f"{BACKEND_URL}/blood-sugar", headers=headers, json=payload)
                    if response.status_code == 201:
                        st.success("Data berhasil disimpan!")
                        result = response.json()
                        
                        # Tampilkan rekomendasi dan notifikasi yang diterima dari backend
                        st.info(f"**Rekomendasi:** {result.get('recommendation', {}).get('message', 'Tidak ada.')}")
                        if result.get('notification'):
                            st.warning(f"**PERINGATAN:** {result.get('notification')}", icon="⚠️")
                    else:
                        st.error(f"Gagal menyimpan data: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Gagal terhubung ke server backend.")

with col2:
    st.subheader("Riwayat Pengukuran Anda")
    if st.button("Tampilkan / Refresh Riwayat", use_container_width=True):
        headers = get_auth_header()
        if headers:
            try:
                response = requests.get(f"{BACKEND_URL}/blood-sugar", headers=headers)
                if response.status_code == 200:
                    readings = response.json()
                    if readings:
                        df = pd.DataFrame(readings)
                        # Format kolom agar lebih mudah dibaca
                        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%d %b %Y, %H:%M')
                        df.rename(columns={'timestamp': 'Waktu', 'value': 'Kadar Gula', 'condition': 'Kondisi', 'notes': 'Catatan'}, inplace=True)
                        st.dataframe(df[['Waktu', 'Kadar Gula', 'Kondisi', 'Catatan']], use_container_width=True)
                    else:
                        st.info("Belum ada riwayat pengukuran.")
                else:
                    st.error("Gagal mengambil riwayat.")
            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke server backend.")