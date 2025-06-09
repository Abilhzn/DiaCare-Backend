def get_recommendation_service(age: int, glucose: int, condition: str, category: str) -> dict:
    if not isinstance(glucose, int) or glucose < 40 or glucose > 600:
        return {"status": "error", "message": "Masukkan ulang angka hasil tes gula darah. Pastikan dalam rentang 40-600."}

    if glucose < 60:
        return {"status": "warning", "message": "Hipoglikemia berat. Segera konsumsi karbohidrat cepat serap dan hubungi tenaga medis!"}
    elif glucose > 300:
        return {"status": "warning", "message": "Hiperglikemia berat. Minum air putih dan segera konsultasikan ke dokter!"}

    recommendation_message = ""

    if age >= 50:  # Lansia
        if category == "diabetes":
            if condition == "sebelum":
                if glucose < 80:
                    recommendation_message = "Gula darah Anda rendah. Segera konsumsi 15 gram karbohidrat cepat serap (permen, jus buah, atau tablet glukosa). Periksa ulang dalam 15 menit."
                elif glucose > 125:
                    recommendation_message = "Gula darah Anda tinggi. Minum air putih, kurangi karbohidrat, dan konsultasikan ke dokter jika kondisi berulang."
            elif condition == "sesudah":
                if glucose < 140:
                    recommendation_message = "Gula darah Anda rendah. Segera konsumsi 15 gram karbohidrat cepat serap (permen, jus buah, atau tablet glukosa)."
                elif glucose > 199:
                    recommendation_message = "Gula darah Anda tinggi. Hindari makanan manis, tetap hidrasi, dan konsultasikan ke dokter untuk evaluasi pengobatan."
        elif category == "pradiabetes":
            if condition == "sebelum":
                if glucose < 100:
                    recommendation_message = "Gula darah Anda sedikit rendah. Konsumsi camilan sehat dan evaluasi jadwal makan."
                elif glucose > 125:
                    recommendation_message = "Gula darah Anda tinggi. Batasi karbohidrat sederhana dan pertimbangkan konsultasi gizi."
            elif condition == "sesudah":
                if glucose < 140:
                    recommendation_message = "Gula darah Anda sedikit rendah. Konsumsi makanan ringan sehat dan pantau kembali."
                elif glucose > 199:
                    recommendation_message = "Gula darah Anda tinggi. Jaga pola makan dan pertimbangkan konsultasi gizi."
        elif category == "sehat":
            if condition == "sebelum":
                if glucose < 90:
                    recommendation_message = "Gula darah Anda sedikit rendah. Pastikan tidak melewatkan makan dan konsumsi camilan sehat."
                elif glucose > 130:
                    recommendation_message = "Gula darah Anda cukup tinggi. Kurangi asupan gula dan perbanyak minum air putih."
            elif condition == "sesudah":
                if glucose < 81:
                    recommendation_message = "Gula darah Anda rendah. Pertimbangkan konsumsi makanan sumber energi cepat serap."
                elif glucose > 139:
                    recommendation_message = "Gula darah Anda cukup tinggi. Hindari konsumsi gula berlebih dan lakukan aktivitas fisik ringan."
    else:  # Non-lansia
        if age <= 5:
            batas_rendah_sebelum = 100
            batas_tinggi_sebelum = 180
            batas_rendah_sesudah = 100 
            batas_tinggi_sesudah = 200 
        elif age <= 12:
            batas_rendah_sebelum = 70
            batas_tinggi_sebelum = 150
            batas_rendah_sesudah = 90
            batas_tinggi_sesudah = 180
        elif age <= 19:
            batas_rendah_sebelum = 70
            batas_tinggi_sebelum = 130
            batas_rendah_sesudah = 90
            batas_tinggi_sesudah = 180 
        else:  # Dewasa
            batas_rendah_sebelum = 70
            batas_tinggi_sebelum = 99
            batas_rendah_sesudah = 70
            batas_tinggi_sesudah = 140 

        if condition == "sebelum":
            if glucose < batas_rendah_sebelum:
                recommendation_message = f"Gula darah Anda rendah ({glucose} mg/dL). Konsumsi 15 gram karbohidrat cepat serap dan cek ulang dalam 15 menit."
            elif glucose > batas_tinggi_sebelum:
                recommendation_message = f"Gula darah Anda tinggi ({glucose} mg/dL). Minum air putih dan batasi asupan karbohidrat sederhana."
        elif condition == "sesudah":
            if glucose < batas_rendah_sesudah:
                recommendation_message = f"Gula darah Anda rendah ({glucose} mg/dL). Konsumsi makanan manis dan cek kembali setelah 15 menit."
            elif glucose > batas_tinggi_sesudah:
                recommendation_message = f"Gula darah Anda tinggi ({glucose} mg/dL). Hindari konsumsi gula berlebih dan lakukan aktivitas ringan."

    if recommendation_message:
        return {"status": "success", "message": recommendation_message}
    else:
        return {"status": "none", "message": None}
