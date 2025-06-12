import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000" # Pastikan URL ini sama

# ==========================================================
#                      PENJAGA HALAMAN
# Letakkan ini di bagian paling atas setiap file di folder /pages
# ==========================================================
if 'is_logged_in' not in st.session_state or not st.session_state['is_logged_in']:
    st.error("🚫 Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.write("Silakan kembali ke halaman utama untuk Login.")
    st.stop() # Hentikan eksekusi sisa halaman
# ==========================================================


# Jika lolos dari penjaga, sisa halaman akan ditampilkan
st.title("🩸 Catat dan Pantau Gula Darah")

# --- Form Input Data ---
with st.form("data_gula_form"):
    kadar_gula = st.number_input("Kadar Gula Darah (mg/dL)", min_value=0)
    kondisi = st.selectbox("Kondisi Pengukuran", ["sebelum_makan", "sesudah_makan", "puasa", "lainnya"])
    catatan = st.text_area("Catatan (optional)")
    simpan_button = st.form_submit_button("Simpan Data")

    if simpan_button:
        # AMBIL TOKEN DARI BUKU CATATAN AJAIB
        token = st.session_state['token']
        
        # Buat header otorisasi
        headers = {'Authorization': f'Bearer {token}'}
        
        # Siapkan data untuk dikirim
        payload = {
            "kadar_gula": kadar_gula,
            "kondisi": kondisi,
            "catatan": catatan
        }
        
        # Kirim data ke API dengan menyertakan header
        response = requests.post(f"{API_URL}/catat-gula-darah", json=payload, headers=headers)
        
        if response.status_code == 201 or response.status_code == 200:
            st.success("Data berhasil disimpan!")
        else:
            # Ini akan menangkap error "Invalid token" dari backend jika ada masalah
            st.error(f"Gagal menyimpan data: {response.json().get('message', 'Terjadi kesalahan')}")

# --- Riwayat Pengukuran ---
st.header("Riwayat Pengukuran Anda")
# ... kode untuk menampilkan riwayat ...