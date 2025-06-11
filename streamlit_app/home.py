import streamlit as st
import requests
import json
import time

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

# Jika SUDAH login, tampilkan halaman sambutan dan menu
if st.session_state.auth_token:
    with st.sidebar:
        st.subheader(f"Selamat Datang,")
        st.markdown(f"**{st.session_state.user_name}**!")
        st.divider()
        if st.button("Keluar", use_container_width=True, type="primary"):
            st.session_state.auth_token = None
            st.session_state.user_name = None
            st.rerun()
    
    st.title("Selamat Datang Kembali di DiaCare! 🩺")
    st.markdown("Gunakan menu di samping untuk menavigasi fitur-fitur yang tersedia.")
    st.info("Anda sudah masuk. Silakan pilih halaman dari sidebar di sebelah kiri.", icon="👈")

# Jika BELUM login, tampilkan pilihan Login atau Registrasi
else:
    st.title("Selamat Datang di DiaCare! 🩺")
    
    # --- Membuat Dua Tab: Satu untuk Login, Satu untuk Registrasi ---
    login_tab, register_tab = st.tabs(["Masuk (Login)", "Daftar Akun Baru (Registrasi)"])

    # --- KONTEN TAB LOGIN ---
    with login_tab:
        st.subheader("Silakan Masuk ke Akun Anda")
        with st.form("login_form"):
            email_login = st.text_input("Email", key="login_email")
            password_login = st.text_input("Password", type="password", key="login_password")
            
            if st.form_submit_button("Masuk", use_container_width=True, type="primary"):
                if not email_login or not password_login:
                    st.error("Email dan Password tidak boleh kosong.")
                else:
                    try:
                        payload = {"email": email_login, "password": password_login}
                        response = requests.post(f"{BACKEND_URL}/auth/login", json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.auth_token = data.get("auth_token")
                            # Ambil nama dari profil jika ada, jika tidak dari username
                            profile_data = data.get("user", {}).get("profile", {})
                            st.session_state.user_name = profile_data.get("full_name") if profile_data and profile_data.get("full_name") else data.get("user", {}).get("username")
                            
                            st.rerun() # Muat ulang halaman untuk masuk ke state "sudah login"
                        else:
                            st.error(f"Gagal login: {response.json().get('message', 'Error tidak diketahui')}")
                    except requests.exceptions.ConnectionError:
                        st.error("Gagal terhubung ke server backend. Pastikan server sudah berjalan.")

    # --- KONTEN TAB REGISTRASI ---
    with register_tab:
        st.subheader("Buat Akun Baru Anda")
        with st.form("register_form"):
            username_reg = st.text_input("Username (untuk login, tanpa spasi)", key="reg_username")
            fullname_reg = st.text_input("Nama Lengkap", key="reg_fullname")
            email_reg = st.text_input("Email", key="reg_email")
            password_reg = st.text_input("Password", type="password", key="reg_password")
            confirm_password_reg = st.text_input("Konfirmasi Password", type="password", key="reg_confirm_password")

            if st.form_submit_button("Daftar", use_container_width=True):
                # Validasi di sisi frontend
                if not all([username_reg, fullname_reg, email_reg, password_reg, confirm_password_reg]):
                    st.error("Semua field wajib diisi.")
                elif password_reg != confirm_password_reg:
                    st.error("Password dan konfirmasi password tidak cocok.")
                else:
                    try:
                        # Kirim request ke endpoint registrasi di backend
                        payload = {
                            "username": username_reg,
                            "email": email_reg,
                            "password": password_reg,
                            "full_name": fullname_reg
                        }
                        response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)

                        if response.status_code == 201: # 201 Created
                            st.success("Registrasi berhasil! Anda akan diarahkan ke tab Login untuk masuk.")
                            st.info("Silakan pindah ke tab 'Masuk (Login)' dan masuk dengan email dan password yang baru saja Anda daftarkan.")
                        else:
                            st.error(f"Gagal mendaftar: {response.json().get('message', 'Error tidak diketahui')}")
                    except requests.exceptions.ConnectionError:
                        st.error("Gagal terhubung ke server backend.")