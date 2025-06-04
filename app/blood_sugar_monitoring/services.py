# services.py
import datetime

# =============================
# 📦 Data Storage (simulasi database)
# =============================
riwayat_gula_darah = []

def catat_data(nilai):
    """Mencatat data gula darah ke dalam riwayat."""
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    riwayat_gula_darah.append({"waktu": waktu, "nilai": nilai})
    return True # Indikasi sukses

def dapatkan_riwayat():
    """Mengembalikan seluruh riwayat gula darah."""
    return riwayat_gula_darah

def ubah_data(indeks, nilai_baru):
    """Mengubah nilai data gula darah pada indeks tertentu."""
    if indeks < 0 or indeks >= len(riwayat_gula_darah):
        raise IndexError("Nomor data tidak valid.")
    riwayat_gula_darah[indeks]['nilai'] = nilai_baru
    return True # Indikasi sukses

# =============================
# 🧪 Validasi Input
# =============================
def validasi_input_gula_darah(input_str):
    """
    Melakukan validasi terhadap input kadar gula darah.
    Akan melempar ValueError jika input tidak valid.
    """
    if input_str == "":
        raise ValueError("Input tidak boleh kosong.")
    try:
        nilai = float(input_str)
    except ValueError:
        raise ValueError("Input harus berupa angka.")
    
    if nilai < 20 or nilai > 600:
        raise ValueError("Nilai gula darah tidak wajar, periksa kembali inputan anda.")
    
    return nilai