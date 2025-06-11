import streamlit as st
import requests
import json

# --- KONFIGURASI & FUNGSI BANTUAN ---
st.set_page_config(
    page_title="DiaCare Home",
    page_icon="🏠",
    layout="centered"
)

BACKEND_URL = "http://127.0.0.1:5000/api"

# Inisialisasi session state jika belum ada
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- TAMPILAN UTAMA ---

# Jika sudah login, tampilkan pesan selamat datang dan tombol logout di sidebar
if st.session_state.auth_token:
    with st.sidebar:
        st.subheader(f"Selamat Datang,")
        st.markdown(f"**{st.session_state.user_name}**!")
        st.divider()
        if st.button("Keluar", use_container_width=True):
            st.session_state.auth_token = None
            st.session_state.user_name = None
            st.rerun()
    
    st.title("Selamat Datang di DiaCare! 🩺")
    st.markdown("Gunakan menu di samping untuk menavigasi fitur-fitur yang tersedia.")
    st.info("Anda sudah masuk. Silakan pilih halaman dari sidebar di sebelah kiri.", icon="👈")

# Jika belum login, tampilkan form login
else:
    st.title("Selamat Datang di DiaCare! 🩺")
    st.header("Silakan Masuk untuk Melanjutkan")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Masuk"):
            if not email or not password:
                st.error("Email dan Password tidak boleh kosong.")
            else:
                try:
                    response = requests.post(f"{BACKEND_URL}/auth/login", json={"email": email, "password": password})
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.auth_token = data.get("auth_token")
                        st.session_state.user_name = data.get("user", {}).get("name")
                        st.rerun()

                        # --- LOGIKA BARU DI SINI ---
                        user_status = data.get("user_status")
                        
                        if user_status == "new_user_profile_incomplete":
                            st.success("Login berhasil! Selamat datang di DiaCare.")
                            st.warning("Profil kesehatan Anda belum lengkap. Silakan lengkapi profil Anda terlebih dahulu untuk menggunakan semua fitur.")
                            # Di aplikasi multi-halaman, kamu bisa mengarahkan mereka ke halaman profil
                            # st.switch_page("pages/4_Profil_Saya.py") # Contoh jika pakai fitur switch_page Streamlit terbaru
                        else:
                            st.success("Login berhasil! Selamat datang kembali.")
                        
                        # Simpan data profil ke session state jika perlu
                        st.session_state.profile = data.get("user", {}).get("profile")
                        
                        # Tunggu sesaat lalu muat ulang halaman untuk menampilkan menu utama
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"Gagal login: {response.json().get('message', 'Error tidak diketahui')}")
                except requests.exceptions.ConnectionError:
                    st.error("Gagal terhubung ke server backend. Pastikan server sudah berjalan.")