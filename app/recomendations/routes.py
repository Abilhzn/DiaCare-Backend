# Logika rekomendasi berdasarkan nilai gula darah
# Sesuai skenario SC016, SC017, SC018, SC019 [cite: 16]

def get_recommendations_for_reading(sugar_level_value):
    if sugar_level_value is None:
        return None # Atau "Data gula darah tidak tersedia."

    try:
        value = float(sugar_level_value)
    except ValueError:
        return "Nilai gula darah tidak valid."

    if value > 200: # SC016: Gula tinggi [cite: 16]
        if value > 250: # SC019: Kondisi ekstrem (tinggi) [cite: 16]
             return "Kadar gula sangat tinggi! Minum air putih, kurangi karbohidrat segera. Segera konsultasi dengan dokter jika tidak membaik atau ada gejala lain."
        return "Kadar gula Anda tinggi. Disarankan untuk minum air putih yang cukup dan kurangi asupan karbohidrat serta gula."
    elif value < 70: # SC017: Gula rendah [cite: 16]
        if value < 55: # SC019: Kondisi ekstrem (rendah) [cite: 16]
            return "Kadar gula sangat rendah! Segera konsumsi sumber glukosa cepat (15-20g) seperti permen, madu, atau jus buah. Jika tidak membaik dalam 15 menit, ulangi dan segera cari bantuan medis."
        return "Kadar gula Anda rendah. Disarankan untuk mengonsumsi sumber glukosa cepat saji seperti permen, tablet glukosa, atau satu sendok madu."
    elif 70 <= value <= 130: # SC018: Normal [cite: 16] (rentang normal bisa disesuaikan)
        return "Kadar gula darah Anda dalam rentang normal. Pertahankan pola hidup sehat!"
    elif 130 < value <= 200: # Di atas normal tapi belum sangat tinggi
        return "Kadar gula darah Anda sedikit di atas normal. Perhatikan asupan makanan Anda, terutama karbohidrat dan gula. Tingkatkan aktivitas fisik."
    else: # Jika ada kondisi lain yang tidak tercover
        return "Tidak ada rekomendasi spesifik. Pantau terus kondisi Anda dan konsultasikan dengan dokter jika ada keluhan."

# Jika rekomendasi juga berdasarkan hasil prediksi diabetes, tambahkan fungsi lain:
# def get_recommendations_for_diabetes_prediction(prediction_result):
#     if prediction_result == "Tinggi":
#         return "Risiko diabetes Anda tinggi. Segera konsultasikan dengan dokter untuk pemeriksaan lebih lanjut dan rencana pengelolaan."
#     elif prediction_result == "Sedang":
#         return "Risiko diabetes Anda sedang. Tingkatkan gaya hidup sehat dengan pola makan seimbang dan olahraga teratur. Lakukan pemeriksaan rutin."
#     else: # Rendah
#         return "Risiko diabetes Anda rendah. Tetap jaga gaya hidup sehat."