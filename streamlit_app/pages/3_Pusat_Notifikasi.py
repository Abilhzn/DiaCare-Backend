import streamlit as st
import requests
import pandas as pd
from config import BACKEND_URL # <-- Menggunakan dari config

st.set_page_config(page_title="Pusat Notifikasi", page_icon="🔔", layout="centered")

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
st.title("🔔 Pusat Notifikasi")
st.markdown("Berikut adalah riwayat peringatan dan notifikasi penting untuk akun Anda.")

# Tombol refresh
if st.button("Tampilkan / Refresh Notifikasi", use_container_width=True):
    # Hapus cache notifikasi agar dimuat ulang
    if 'notifications_list' in st.session_state:
        del st.session_state['notifications_list']

# Logika untuk memuat dan menampilkan notifikasi
# Ini akan berjalan otomatis saat halaman dibuka pertama kali
if 'notifications_list' not in st.session_state:
    headers = get_auth_header()
    if headers:
        with st.spinner("Memuat notifikasi..."):
            try:
                response = requests.get(f"{BACKEND_URL}/notifications", headers=headers)
                if response.status_code == 200:
                    # Simpan hasil (bahkan jika kosong) ke session state
                    st.session_state.notifications_list = response.json()
                else:
                    st.error("Gagal mengambil notifikasi.")
                    st.session_state.notifications_list = None # Tandai sebagai error
            except Exception as e:
                st.error(f"Gagal terhubung ke server: {e}")
                st.session_state.notifications_list = None

# Tampilkan notifikasi dari session_state
if 'notifications_list' in st.session_state and st.session_state.notifications_list is not None:
    notifications = st.session_state.notifications_list
    if notifications:
        st.divider()
        # Urutkan notifikasi dari yang terbaru
        sorted_notifications = sorted(notifications, key=lambda x: x['created_at'], reverse=True)
        for notif in sorted_notifications:
            ts = pd.to_datetime(notif['created_at']).strftime('%d %b %Y, %H:%M')
            st.warning(f"**Pukul {ts}:** {notif['message']}", icon="⚠️")
    else:
        st.success("Tidak ada notifikasi untuk ditampilkan. Semuanya aman!", icon="✅")