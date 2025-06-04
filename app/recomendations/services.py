# app/recommendations/services.py (Revisi V.2)

from datetime import date

def get_recommendation_service(age: int, glucose: int, condition: str, category: str) -> dict:
    """
    Memberikan rekomendasi tindakan berdasarkan usia, kadar glukosa, kondisi tes, dan kategori kesehatan.
    Asumsi: 'condition' (sebelum/sesudah makan) disediakan oleh modul pemantauan atau sudah dikelola konteksnya.

    Args:
        age (int): Usia pengguna.
        glucose (int): Kadar glukosa darah.
        condition (str): Kondisi tes ('sebelum' makan atau 'sesudah' makan). Ini diasumsikan datang dari modul pemantauan.
        category (str): Kategori kesehatan pengguna ('sehat', 'pradiabetes', 'diabetes').

    Returns:
        dict: Kamus berisi status (success/error) dan pesan rekomendasi.
    """
    # --- Validasi Input Gula Darah ---
    if not isinstance(glucose, int) or glucose < 40 or glucose > 600:
        return {"status": "error", "message": "Masukkan ulang angka hasil tes gula darah. Pastikan dalam rentang 40-600."}

    # --- Validasi Kondisi dan Kategori ---
    valid_conditions = ["sebelum", "sesudah"]
    valid_categories = ["sehat", "pradiabetes", "diabetes"]

    if condition not in valid_conditions:
        # Ini penting: Jika condition datang dari pemantauan, error ini menandakan masalah di modul pemantauan
        return {"status": "error", "message": "Kondisi tes ('sebelum' atau 'sesudah') tidak valid, periksa data dari modul pemantauan."}
    if category not in valid_categories:
        return {"status": "error", "message": "Kategori kesehatan tidak valid. Pilih 'sehat', 'pradiabetes', atau 'diabetes'."}

    # --- Kondisi Ekstrem ---
    if glucose < 60:
        return {"status": "warning", "message": "Hipoglikemia. Segera periksakan ke dokter!!"}
    elif glucose > 300:
        return {"status": "warning", "message": "Hiperglikemia. Segera periksakan ke dokter!!"}

    # --- Rekomendasi Berdasarkan Usia ---
    recommendation_message = ""

    if age >= 50:  # Lansia
        if category == "diabetes":
            if condition == "sebelum":
                if glucose < 80:
                    recommendation_message = "Gula darah anda rendah, segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
                elif glucose > 125:
                    recommendation_message = "Gula darah anda tinggi, Minum air putih, kurangi karbohidrat, dan konsultasi dengan dokter untuk penyesuaian obat jika perlu."
                else:
                    recommendation_message = "Gula darah Anda dalam rentang target (80-125 mg/dL). Pertahankan pola hidup sehat."
            elif condition == "sesudah":
                if glucose < 140:
                    # Note: Target gula darah post-meal untuk penderita diabetes mungkin lebih tinggi dari 140
                    # Ini adalah contoh batas, sesuaikan dengan standar medis yang Anda gunakan.
                    recommendation_message = "Gula darah anda rendah, segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
                elif glucose > 199:
                    recommendation_message = "Gula darah anda tinggi, Minum air putih, kurangi karbohidrat, dan konsultasi dengan dokter untuk penyesuaian obat jika perlu."
                else:
                    recommendation_message = "Gula darah Anda dalam rentang target (140-199 mg/dL). Pertahankan pola hidup sehat."
        elif category == "pradiabetes":
            if condition == "sebelum":
                if glucose < 100:
                    recommendation_message = "Gula darah anda rendah, segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
                elif glucose > 125:
                    recommendation_message = "Gula darah anda tinggi, Minum air putih, kurangi karbohidrat, dan pertimbangkan konsultasi gizi untuk pencegahan diabetes."
                else:
                    recommendation_message = "Gula darah Anda dalam rentang pradiabetes yang baik (100-125 mg/dL). Tetap jaga pola makan dan aktivitas fisik."
            elif condition == "sesudah":
                if glucose < 140:
                    recommendation_message = "Gula darah anda rendah, segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
                elif glucose > 199:
                    recommendation_message = "Gula darah anda tinggi, Minum air putih, kurangi karbohidrat, dan pertimbangkan konsultasi gizi untuk pencegahan diabetes."
                else:
                    recommendation_message = "Gula darah Anda dalam rentang pradiabetes yang baik (140-199 mg/dL). Tetap jaga pola makan dan aktivitas fisik."
        elif category == "sehat":
            if condition == "sebelum":
                if glucose < 90:
                    recommendation_message = "Gula darah anda rendah, segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
                elif glucose > 130:
                    recommendation_message = "Gula darah anda tinggi, Minum air putih, kurangi karbohidrat."
                else:
                    recommendation_message = "Gula darah Anda normal dan sehat (90-130 mg/dL). Pertahankan gaya hidup seimbang."
            elif condition == "sesudah":
                if glucose < 81:
                    recommendation_message = "Gula darah anda rendah, segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
                elif glucose > 139:
                    recommendation_message = "Gula darah anda tinggi, Minum air putih, kurangi karbohidrat."
                else:
                    recommendation_message = "Gula darah Anda normal dan sehat (81-139 mg/dL). Pertahankan gaya hidup seimbang."
    else:  # Non-lansia (anak-anak / dewasa < 50)
        # Asumsi untuk non-lansia, kategori "sehat" adalah default jika tidak ada riwayat
        # Jika ada kategori pradiabetes/diabetes untuk non-lansia, Anda perlu menambahkan logika serupa di sini.
        
        # Batas untuk non-lansia (sesuaikan jika kategori 'pradiabetes'/'diabetes' juga berlaku untuk usia ini)
        batas_rendah_sebelum: int
        batas_tinggi_sebelum: int
        batas_rendah_sesudah: int
        batas_tinggi_sesudah: int

        # Batasan Umum untuk Non-Lansia Sehat (sebelum makan)
        if age <= 5:
            batas_rendah_sebelum = 80
            batas_tinggi_sebelum = 180
            batas_rendah_sesudah = 80 # Batas bawah umum untuk anak setelah makan
            batas_tinggi_sesudah = 200 # Batas atas umum untuk anak setelah makan
        elif age <= 12:
            batas_rendah_sebelum = 80
            batas_tinggi_sebelum = 180
            batas_rendah_sesudah = 80
            batas_tinggi_sesudah = 200
        elif age <= 19:
            batas_rendah_sebelum = 70
            batas_tinggi_sebelum = 150
            batas_rendah_sesudah = 70
            batas_tinggi_sesudah = 170 # Remaja mungkin sedikit lebih rendah dari anak kecil
        else:  # Dewasa (>19 dan <50)
            batas_rendah_sebelum = 70
            batas_tinggi_sebelum = 130
            batas_rendah_sesudah = 70
            batas_tinggi_sesudah = 140 # Dewasa sehat setelah makan

        if condition == "sebelum":
            if glucose < batas_rendah_sebelum:
                recommendation_message = f"Gula darah anda rendah ({glucose} mg/dL) sebelum makan. Segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
            elif glucose > batas_tinggi_sebelum:
                recommendation_message = f"Gula darah anda tinggi ({glucose} mg/dL) sebelum makan. Minum air putih, kurangi karbohidrat."
            else:
                recommendation_message = f"Gula darah Anda normal ({glucose} mg/dL) sebelum makan untuk usia Anda. Pertahankan gaya hidup sehat."
        elif condition == "sesudah":
            if glucose < batas_rendah_sesudah:
                recommendation_message = f"Gula darah anda rendah ({glucose} mg/dL) setelah makan. Segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
            elif glucose > batas_tinggi_sesudah:
                recommendation_message = f"Gula darah anda tinggi ({glucose} mg/dL) setelah makan. Minum air putih, kurangi karbohidrat."
            else:
                recommendation_message = f"Gula darah Anda normal ({glucose} mg/dL) setelah makan untuk usia Anda. Pertahankan gaya hidup sehat."
        
    # Jika semua kondisi terpenuhi dan ada pesan rekomendasi, kirimkan sebagai sukses
    if recommendation_message:
        return {"status": "success", "message": recommendation_message}
    else:
        # Ini seharusnya tidak tercapai jika semua kondisi tercakup, tapi sebagai fallback
        return {"status": "error", "message": "Tidak dapat menentukan rekomendasi. Periksa input dan logika."}