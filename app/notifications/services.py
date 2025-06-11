# app/recommendations/services.py (Revisi V.2)

from datetime import date

def get_recommendation_service(age: int, glucose: int, condition: str, category: str) -> dict:
    """
    Memberikan rekomendasi tindakan berdasarkan usia, kadar glukosa, kondisi tes, dan kategori kesehatan.
    """
    # --- Validasi Input ---
    if not isinstance(glucose, int) or glucose < 40 or glucose > 600:
        return {"status": "error", "message": "Masukkan angka gula darah antara 40 - 600 mg/dL."}

    valid_conditions = ["sebelum", "sesudah"]
    valid_categories = ["sehat", "pradiabetes", "diabetes"]

    if condition not in valid_conditions:
        return {"status": "error", "message": "Kondisi harus 'sebelum' atau 'sesudah'."}
    if category not in valid_categories:
        return {"status": "error", "message": "Kategori tidak valid. Gunakan 'sehat', 'pradiabetes', atau 'diabetes'."}

    # --- Hipoglikemia & Hiperglikemia ---
    if glucose < 60:
        return {"status": "warning", "message": "Hipoglikimia. Segera periksakan ke dokter!!"}
    elif glucose > 300:
        return {"status": "warning", "message": "Hiperglikimia. Segera periksakan ke dokter!!"}

    is_lansia = age >= 50
    recommendation = ""

    # --- Rentang nilai berdasarkan kondisi dan kategori untuk lansia ---
    if is_lansia:
        batas = {
            "sehat": {"sebelum": (90, 130), "sesudah": (81, 139)},
            "pradiabetes": {"sebelum": (100, 125), "sesudah": (140, 199)},
            "diabetes": {"sebelum": (80, 125), "sesudah": (140, 199)}
        }
    else:
        # Untuk non-lansia, default: sehat
        if age <= 5:
            batas = {"sehat": {"sebelum": (80, 180), "sesudah": (80, 200)}}
        elif age <= 12:
            batas = {"sehat": {"sebelum": (80, 180), "sesudah": (80, 200)}}
        elif age <= 19:
            batas = {"sehat": {"sebelum": (70, 150), "sesudah": (70, 170)}}
        else:
            batas = {"sehat": {"sebelum": (70, 130), "sesudah": (70, 140)}}

    # --- Ambil rentang sesuai kategori dan kondisi ---
    if category in batas:
        low, high = batas[category][condition]
    else:
        low, high = batas["sehat"][condition]

    if glucose < low:
        recommendation = "Gula darah anda rendah, segera konsumsi karbohidrat seperti permen, jus buah, atau tablet glukosa."
    elif glucose > high:
        recommendation = "Gula darah anda tinggi, Minum air putih, kurangi karbohidrat."
    else:
        recommendation = "Pertahankan Kondisi Kesehatan Anda"

    return {"status": "success", "message": recommendation}
