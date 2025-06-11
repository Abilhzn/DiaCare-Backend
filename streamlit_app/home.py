# streamlit_app/Home.py

import streamlit as st
import requests
import json

# URL API backend-mu. Pastikan ini benar.
BACKEND_URL = "http://127.0.0.1:5000/api"

st.title("Selamat Datang di DiaCare! 🩺")

# Logika untuk berkomunikasi dengan backend
# Contoh: Membuat form login
with st.form("login_form"):
    st.write("Silakan Masuk")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button(label="Masuk")

    if submit_button:
        try:
            # Kirim request POST ke endpoint login di backend
            response = requests.post(f"{BACKEND_URL}/auth/login", json={
                "email": email,
                "password": password
            })
            
            if response.status_code == 200:
                st.success("Login Berhasil!")
                # Kamu bisa menyimpan token di st.session_state untuk request selanjutnya
                st.session_state['auth_token'] = response.json().get('auth_token')
                st.write(response.json()) # Tampilkan respons dari backend
            else:
                st.error(f"Gagal Login: {response.json().get('message')}")

        except requests.exceptions.ConnectionError:
            st.error("Gagal terhubung ke server backend. Pastikan backend sudah berjalan.")