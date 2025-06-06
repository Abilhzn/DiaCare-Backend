# routes.py
from . import services # Mengimpor fungsi dari services.py dalam paket yang sama

# =============================
# ✍️ Fitur: Input Gula Darah
# =============================
def fitur_input():
    """Menangani alur input gula darah dari pengguna."""
    while True:
        try:
            input_str = input("Masukkan kadar gula darah Anda (mg/dL): ").strip()
            nilai = services.validasi_input_gula_darah(input_str)
            
            services.catat_data(nilai)
            print("✅ Data berhasil dicatat.")
            break 
        except ValueError as e:
            print(f"❌ Error: {e}. Silakan coba lagi.")

# =============================
# 📜 Fitur: Lihat Riwayat
# =============================
def fitur_lihat_riwayat():
    """Menampilkan riwayat gula darah kepada pengguna."""
    riwayat = services.dapatkan_riwayat()
    if not riwayat:
        print("Belum ada data gula darah.")
    else:
        print("\n📜 Riwayat Gula Darah:")
        for i, data in enumerate(riwayat):
            print(f"{i+1}. {data['waktu']} - {data['nilai']} mg/dL")

# =============================
# ✏️ Fitur: Edit Data
# =============================
def fitur_edit_data():
    """Menangani alur edit data gula darah oleh pengguna."""
    fitur_lihat_riwayat() # Tampilkan riwayat terlebih dahulu
    while True:
        try:
            indeks_str = input("\nMasukkan nomor data yang ingin diedit: ").strip()
            if not indeks_str.isdigit():
                raise ValueError("Nomor data harus berupa angka.")
            indeks = int(indeks_str) - 1
            
            # Memastikan indeks valid sebelum meminta nilai baru
            if indeks < 0 or indeks >= len(services.dapatkan_riwayat()):
                raise IndexError("Nomor tidak valid.")

            input_baru = input("Masukkan nilai baru (mg/dL): ").strip()
            nilai_baru = services.validasi_input_gula_darah(input_baru)

            services.ubah_data(indeks, nilai_baru)
            print("✏️ Data berhasil diperbarui.")
            break
        except (ValueError, IndexError) as e:
            print(f"❌ Error: {e}. Silakan coba lagi.")