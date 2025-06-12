# 🩺 DiaCare - Backend API

Selamat datang di repository backend untuk aplikasi DiaCare. Proyek ini menyediakan API untuk deteksi risiko diabetes, pemantauan gula darah, rekomendasi tindakan, dan notifikasi.

## Fitur Utama

-   Otentikasi Pengguna (Registrasi & Login dengan JWT)
-   Manajemen Profil Kesehatan Pengguna
-   Prediksi Risiko Diabetes menggunakan Model Machine Learning
-   Pencatatan & Riwayat Kadar Gula Darah
-   Rekomendasi Tindakan Cerdas berdasarkan kondisi pengguna
-   Sistem Notifikasi Peringatan untuk kondisi darurat

---

## Panduan Setup & Instalasi

Berikut adalah langkah-langkah untuk menjalankan proyek ini di lingkungan lokal.

### Prasyarat

-   Python 3.8+
-   pip (Package Installer for Python)
-   Git

### Langkah-langkah Instalasi

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/usernamekalian/DiaCare-Backend.git](https://github.com/usernamekalian/DiaCare-Backend.git)
    cd DiaCare-Backend
    ```

2.  **Buat dan Aktifkan Virtual Environment:**
    ```bash
    # Membuat venv
    python -m venv venv

    # Mengaktifkan venv (Windows)
    venv\Scripts\activate

    # Mengaktifkan venv (macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Jika Menggunakan Git LFS)** Pastikan Git LFS terinstal dan tarik file modelnya:
    ```bash
    git lfs install
    git lfs pull
    ```

5.  **Setup File `.env`:**
    * Buat salinan dari file `.env.example` dan beri nama `.env`.
    * Buka file `.env` dan isi semua variabel yang diperlukan, terutama `SECRET_KEY` dan `JWT_SECRET_KEY` dengan nilai acak yang aman.

6.  **Inisialisasi dan Migrasi Database:**
    * Jalankan perintah ini untuk membuat tabel-tabel di databasemu.
    ```bash
    flask db upgrade
    ```
    *(Jika ini pertama kali, kamu mungkin perlu `flask db init` dan `flask db migrate` terlebih dahulu).*

---

## Cara Menjalankan Aplikasi

Kamu perlu membuka **dua terminal** terpisah.

**1. Jalankan Backend Server (Flask):**
Pastikan virtual environment sudah aktif.
```bash
flask run