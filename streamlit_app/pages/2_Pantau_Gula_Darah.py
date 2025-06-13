# pages/1_Pantau_Gula_Darah.py

import streamlit as st
import requests
import pandas as pd
import altair as alt # Library baru untuk charting
from config import BACKEND_URL

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Dashboard Gula Darah", page_icon="🩸", layout="wide")

# --- Fungsi Bantuan ---
def get_auth_header():
    token = st.session_state.get('auth_token')
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}

# --- Penjaga Halaman (Wajib) ---
if not st.session_state.get('auth_token'):
    st.error("🚫 Anda harus login untuk mengakses halaman ini.")
    st.info("Silakan kembali ke halaman Home untuk login.")
    st.stop()

# --- Judul Utama Halaman ---
st.title("🩸 Dashboard Pemantauan Gula Darah")

# --- Membuat Struktur Tabs ---
tab_input, tab_riwayat = st.tabs(["✍️ Input Data Baru", "📈 Riwayat & Visualisasi"])


# ==========================================================
#                   KONTEN UNTUK TAB INPUT
# ==========================================================
with tab_input:
    st.header("Tambah Catatan Pengukuran Baru")
    
    with st.form("new_reading_form"):
        col1, col2 = st.columns(2)
        with col1:
            glucose_value = st.number_input("Kadar Gula Darah (mg/dL)", min_value=20, max_value=600, value=100)
        with col2:
            condition = st.selectbox("Kondisi Pengukuran", 
                                     options=["sebelum_makan", "setelah_makan", "puasa", "sebelum_tidur", "random"], 
                                     index=0)
        
        notes = st.text_area("Catatan (opsional)", placeholder="Contoh: Merasa sedikit pusing setelah makan...")
        
        submitted = st.form_submit_button("Simpan Data Baru", use_container_width=True, type="primary")
        
        if submitted:
            payload = {"value": glucose_value, "condition": condition, "notes": notes}
            with st.spinner("Menyimpan data..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/blood-sugar", headers=get_auth_header(), json=payload)
                    if response.status_code == 200: # Backend mengembalikan 200 setelah diubah
                        st.success("Data berhasil disimpan!")
                        # Ambil data rekomendasi dari respons JSON
                        response_data = response.json()
                        recommendation = response_data.get("recommendation", {}).get("message")
                        
                        if recommendation:
                            st.info(f"💡 Rekomendasi untuk Anda: {recommendation}")

                        # Hapus cache riwayat agar data di tab lain auto-refresh
                        if 'bs_history_df' in st.session_state:
                            del st.session_state['bs_history_df']
                    else:
                        st.error(f"Gagal: {response.json().get('message', response.text)}")
            
                except Exception as e:
                    st.error(f"Koneksi gagal: {e}")

# ==========================================================
#              KONTEN UNTUK TAB RIWAYAT & VISUALISASI
# ==========================================================
with tab_riwayat:
    st.header("Analisis Riwayat Gula Darah Anda")
    
    if st.button("🔄 Tampilkan / Refresh Data"):
        # Jika tombol ditekan, hapus cache agar data dimuat ulang
        if 'bs_history_df' in st.session_state:
            del st.session_state['bs_history_df']

    # Caching data di session_state untuk performa
    if 'bs_history_df' not in st.session_state:
        with st.spinner("Mengambil data riwayat dari server..."):
            try:
                response = requests.get(f"{BACKEND_URL}/blood-sugar", headers=get_auth_header())
                if response.status_code == 200:
                    readings = response.json()
                    # Simpan dataframe ke session state, bahkan jika kosong
                    st.session_state.bs_history_df = pd.DataFrame(readings)
                else:
                    st.error("Gagal mengambil data riwayat.")
                    st.session_state.bs_history_df = pd.DataFrame()
            except Exception as e:
                st.error(f"Koneksi gagal: {e}")
                st.session_state.bs_history_df = pd.DataFrame()

    # Ambil data dari cache
    history_df = st.session_state.bs_history_df

    if not history_df.empty:
        # --- Bagian Visualisasi (Grafik) ---
        st.subheader("Grafik Tren Gula Darah")
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
        chart = alt.Chart(history_df).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X('timestamp:T', title='Waktu Pengukuran'),
            y=alt.Y('value:Q', title='Kadar Gula Darah (mg/dL)', scale=alt.Scale(zero=False)),
            tooltip=['timestamp:T', 'value:Q', 'condition:N', 'notes:N'],
            color=alt.Color('condition:N', title='Kondisi')
        ).properties(title='Tren Kadar Gula Darah Anda dari Waktu ke Waktu').interactive()
        st.altair_chart(chart, use_container_width=True)
        st.divider()
        st.subheader("Tabel Riwayat Pengukuran")
        display_df = history_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%d %b %Y, %H:%M')
        display_df.rename(columns={'timestamp': 'Waktu', 'value': 'Kadar Gula', 'condition': 'Kondisi', 'notes': 'Catatan'}, inplace=True)
        st.dataframe(display_df[['Waktu', 'Kadar Gula', 'Kondisi', 'Catatan']], use_container_width=True)
    else:
        st.info("Belum ada data riwayat. Silakan input data baru di tab sebelah.")
        
# import streamlit as st
# import requests
# import pandas as pd
# from config import BACKEND_URL # <-- Menggunakan dari config

# st.set_page_config(page_title="Pemantauan Gula Darah", page_icon="🩸", layout="wide")

# # --- FUNGSI BANTUAN ---
# def get_auth_header():
#     token = st.session_state.get('auth_token')
#     if not token:
#         return None
#     return {"Authorization": f"Bearer {token}"}

# # --- KUNCI: Penjaga Halaman ---
# if not st.session_state.get('auth_token'):
#     st.warning("Anda harus masuk terlebih dahulu untuk mengakses halaman ini.")
#     st.markdown("Silakan kembali ke halaman **[Home](/)** untuk login.")
#     st.stop()

# # --- TAMPILAN HALAMAN ---
# st.title("🩸 Catat dan Pantau Gula Darah")

# col1, col2 = st.columns([1, 2])

# with col1:
#     st.subheader("Input Data Baru")
#     with st.form("reading_form"):
#         glucose_value = st.number_input("Kadar Gula Darah (mg/dL)", min_value=20, max_value=600, value=100)
#         condition = st.selectbox("Kondisi Pengukuran", ["sebelum_makan", "setelah_makan", "puasa", "sebelum_tidur"])
#         notes = st.text_area("Catatan (opsional)")
        
#         if st.form_submit_button("Simpan Data", use_container_width=True, type="primary"):
#             headers = get_auth_header()
#             if headers:
#                 payload = {"value": glucose_value, "condition": condition, "notes": notes}
#                 with st.spinner("Menyimpan data..."):
#                     try:
#                         response = requests.post(f"{BACKEND_URL}/blood-sugar", headers=headers, json=payload)
#                         if response.status_code == 201:
#                             st.success("Data berhasil disimpan!")
#                             # Auto-refresh riwayat setelah berhasil menyimpan
#                             if 'history_df' in st.session_state:
#                                 del st.session_state['history_df']
#                         else:
#                             st.error(f"Gagal menyimpan data: {response.json().get('message', response.text)}")
#                     except Exception as e:
#                         st.error(f"Terjadi kesalahan koneksi: {e}")

# with col2:
#     st.subheader("Riwayat Pengukuran Anda")
    
#     # Tombol refresh
#     if st.button("Tampilkan / Refresh Riwayat"):
#         # Hapus cache agar data dimuat ulang
#         if 'history_df' in st.session_state:
#             del st.session_state['history_df']

#     # Logika untuk memuat dan menampilkan data
#     if 'history_df' not in st.session_state:
#         headers = get_auth_header()
#         if headers:
#             with st.spinner("Memuat riwayat..."):
#                 try:
#                     response = requests.get(f"{BACKEND_URL}/blood-sugar", headers=headers)
#                     if response.status_code == 200:
#                         readings = response.json()
#                         if readings:
#                             df = pd.DataFrame(readings)
#                             df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%d %b %Y, %H:%M')
#                             df.rename(columns={'timestamp': 'Waktu', 'value': 'Kadar Gula', 'condition': 'Kondisi', 'notes': 'Catatan'}, inplace=True)
#                             st.session_state.history_df = df
#                         else:
#                             st.session_state.history_df = pd.DataFrame() # Simpan dataframe kosong
#                     else:
#                         st.error("Gagal mengambil riwayat.")
#                         st.session_state.history_df = None
#                 except Exception as e:
#                     st.error(f"Gagal terhubung ke server: {e}")
#                     st.session_state.history_df = None

#     # Tampilkan dataframe dari session_state
#     if 'history_df' in st.session_state and st.session_state.history_df is not None:
#         if not st.session_state.history_df.empty:
#             st.dataframe(st.session_state.history_df[['Waktu', 'Kadar Gula', 'Kondisi', 'Catatan']], use_container_width=True)
#         else:
#             st.info("Belum ada riwayat pengukuran.")