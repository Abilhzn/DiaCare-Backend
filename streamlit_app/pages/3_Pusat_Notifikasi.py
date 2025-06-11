import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Pusat Notifikasi", page_icon="🔔", layout="centered")

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

st.title("🔔 Pusat Notifikasi")
st.markdown("Berikut adalah riwayat peringatan penting untuk akun Anda.")

if st.button("Tampilkan / Refresh Notifikasi", use_container_width=True):
    headers = get_auth_header()
    if headers:
        try:
            response = requests.get(f"{BACKEND_URL}/notifications", headers=headers)
            if response.status_code == 200:
                notifications = response.json()
                if notifications:
                    for notif in notifications:
                        ts = pd.to_datetime(notif['created_at']).strftime('%d %b %Y, %H:%M')
                        st.warning(f"**Pukul {ts}:** {notif['message']}", icon="⚠️")
                else:
                    st.success("Tidak ada notifikasi untuk ditampilkan.", icon="✅")
            else:
                st.error("Gagal mengambil notifikasi.")
        except requests.exceptions.ConnectionError:
            st.error("Gagal terhubung ke server backend.")