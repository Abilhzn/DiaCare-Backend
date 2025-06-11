from app.recomendations.services import get_recommendation_service

def generate_notification(age: int, glucose: int, condition: str, category: str) -> dict:
    
    recommendation_result = get_recommendation_service(age, glucose, condition, category)

    status = recommendation_result.get("status")
    message = recommendation_result.get("message")

    # Sesuaikan format notifikasi, misalnya bisa ditampilkan di UI atau dikirim ke sistem lain.
    notification = {
        "status": status,
        "title": "",
        "message": message
    }

    if status == "success":
        notification["title"] = "✅ Rekomendasi Kesehatan"
    elif status == "warning":
        notification["title"] = "⚠️ Peringatan Kadar Glukosa Ekstrem"
    else:
        notification["title"] = "❌ Error"

    return notification