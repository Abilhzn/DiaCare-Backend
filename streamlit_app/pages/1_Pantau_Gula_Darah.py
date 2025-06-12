# pages/1_Pantau_Gula_Darah.py

import streamlit as st
import requests
import pandas as pd
from config import BACKEND_URL # <-- Menggunakan dari config

st.set_page_config(page_title="Pemantauan Gula Darah", page_icon="🩸", layout="wide")

# --- FUNGSI BANTUAN ---
def get_auth_header():
    token = st.session_state.get('auth_token')
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}

# --- KUNCI: Penjaga Halaman ---
if not st.session_state.get('auth_token'):
    st.warning("Anda harus masuk terlebih dahulu untuk mengakses halaman ini.")
    st.markdown("Silakan kembali ke halaman **[Home](/)** untuk login.")
    st.stop()

# --- TAMPILAN HALAMAN ---
st.title("🩸 Catat dan Pantau Gula Darah")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Input Data Baru")
    with st.form("reading_form"):
        glucose_value = st.number_input("Kadar Gula Darah (mg/dL)", min_value=20, max_value=600, value=100)
        condition = st.selectbox("Kondisi Pengukuran", ["sebelum_makan", "setelah_makan", "puasa", "sebelum_tidur"])
        notes = st.text_area("Catatan (opsional)")
        
        if st.form_submit_button("Simpan Data", use_container_width=True, type="primary"):
            headers = get_auth_header()
            if headers:
                payload = {"value": glucose_value, "condition": condition, "notes": notes}
                with st.spinner("Menyimpan data..."):
                    try:
                        response = requests.post(f"{BACKEND_URL}/blood-sugar", headers=headers, json=payload)
                        if response.status_code == 201:
                            st.success("Data berhasil disimpan!")
                            # Auto-refresh riwayat setelah berhasil menyimpan
                            if 'history_df' in st.session_state:
                                del st.session_state['history_df']
                        else:
                            st.error(f"Gagal menyimpan data: {response.json().get('message', response.text)}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan koneksi: {e}")

with col2:
    st.subheader("Riwayat Pengukuran Anda")
    
    # Tombol refresh
    if st.button("Tampilkan / Refresh Riwayat"):
        # Hapus cache agar data dimuat ulang
        if 'history_df' in st.session_state:
            del st.session_state['history_df']

    # Logika untuk memuat dan menampilkan data
    if 'history_df' not in st.session_state:
        headers = get_auth_header()
        if headers:
            with st.spinner("Memuat riwayat..."):
                try:
                    response = requests.get(f"{BACKEND_URL}/blood-sugar", headers=headers)
                    if response.status_code == 200:
                        readings = response.json()
                        if readings:
                            df = pd.DataFrame(readings)
                            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%d %b %Y, %H:%M')
                            df.rename(columns={'timestamp': 'Waktu', 'value': 'Kadar Gula', 'condition': 'Kondisi', 'notes': 'Catatan'}, inplace=True)
                            st.session_state.history_df = df
                        else:
                            st.session_state.history_df = pd.DataFrame() # Simpan dataframe kosong
                    else:
                        st.error("Gagal mengambil riwayat.")
                        st.session_state.history_df = None
                except Exception as e:
                    st.error(f"Gagal terhubung ke server: {e}")
                    st.session_state.history_df = None

    # Tampilkan dataframe dari session_state
    if 'history_df' in st.session_state and st.session_state.history_df is not None:
        if not st.session_state.history_df.empty:
            st.dataframe(st.session_state.history_df[['Waktu', 'Kadar Gula', 'Kondisi', 'Catatan']], use_container_width=True)
        else:
            st.info("Belum ada riwayat pengukuran.")