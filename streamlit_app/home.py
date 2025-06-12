# home.py

import streamlit as st
import requests
from config import BACKEND_URL # <-- Menggunakan dari config

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="DiaCare Home",
    page_icon="🏠",
    layout="centered"
)

# --- INISIALISASI SESSION STATE ---
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- SIDEBAR (Selalu tampil jika sudah login) ---
if st.session_state.auth_token:
    with st.sidebar:
        st.subheader(f"Selamat Datang,")
        st.markdown(f"**{st.session_state.user_name}**!")
        st.divider()
        if st.button("Keluar", use_container_width=True, type="primary"):
            st.session_state.auth_token = None
            st.session_state.user_name = None
            st.success("Anda berhasil keluar.")
            st.rerun()

# --- TAMPILAN UTAMA ---
st.title("Selamat Datang di DiaCare! 🩺")

if st.session_state.auth_token:
    # --- TAMPILAN SETELAH LOGIN ---
    st.markdown("Gunakan menu di samping untuk menavigasi fitur-fitur yang tersedia.")
    st.info("Anda sudah masuk. Silakan pilih halaman dari sidebar di sebelah kiri.", icon="👈")
else:
    # --- TAMPILAN SEBELUM LOGIN (FORM) ---
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
                    with st.spinner("Mencoba masuk..."):
                        try:
                            payload = {"email": email_login, "password": password_login}
                            response = requests.post(f"{BACKEND_URL}/auth/login", json=payload)
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.auth_token = data.get("auth_token")
                                profile_data = data.get("user", {}).get("profile", {})
                                st.session_state.user_name = profile_data.get("full_name", data.get("user", {}).get("username"))
                                st.rerun()
                            else:
                                st.error(f"Gagal login: {response.json().get('message', 'Error tidak diketahui')}")
                        except requests.exceptions.ConnectionError:
                            st.error("Gagal terhubung ke server. Pastikan backend berjalan.")
                        except Exception as e:
                            st.error(f"Terjadi kesalahan: {e}")

    # --- KONTEN TAB REGISTRASI ---
    with register_tab:
        st.subheader("Buat Akun Baru Anda")
        with st.form("register_form"):
            username_reg = st.text_input("Username (tanpa spasi)", key="reg_username")
            fullname_reg = st.text_input("Nama Lengkap", key="reg_fullname")
            email_reg = st.text_input("Email", key="reg_email")
            password_reg = st.text_input("Password", type="password", key="reg_password")
            confirm_password_reg = st.text_input("Konfirmasi Password", type="password", key="reg_confirm_password")

            if st.form_submit_button("Daftar", use_container_width=True):
                if not all([username_reg, fullname_reg, email_reg, password_reg, confirm_password_reg]):
                    st.error("Semua field wajib diisi.")
                elif password_reg != confirm_password_reg:
                    st.error("Password dan konfirmasi password tidak cocok.")
                else:
                    with st.spinner("Mendaftarkan akun..."):
                        try:
                            payload = {
                                "username": username_reg,
                                "email": email_reg,
                                "password": password_reg,
                                "full_name": fullname_reg
                            }
                            response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)

                            if response.status_code == 201:
                                st.success("Registrasi berhasil!")
                                st.info("Silakan pindah ke tab 'Masuk (Login)' untuk masuk.")
                            else:
                                st.error(f"Gagal mendaftar: {response.json().get('message', 'Error tidak diketahui')}")
                        except requests.exceptions.ConnectionError:
                            st.error("Gagal terhubung ke server backend.")
                        except Exception as e:
                            st.error(f"Terjadi kesalahan: {e}")