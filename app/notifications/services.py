from app.recommendations.services import get_recommendation_service
from app.models.notification import Notification
from app.models.base import db

def generate_notification(age: int, glucose: int, condition: str, category: str) -> dict:
    """
    Menghasilkan notifikasi berdasarkan rekomendasi glukosa.

    Args:
        age (int): Usia pengguna.
        glucose (int): Kadar gula.
        condition (str): sebelum/sesudah makan.
        category (str): sehat/pradiabetes/diabetes

    Returns:
        dict: Hasil notifikasi dengan status dan pesan.
    """
    recommendation_result = get_recommendation_service(age, glucose, condition, category)

    status = recommendation_result.get("status")
    message = recommendation_result.get("message")

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

def get_user_notifications(user):
    """
    Mengambil semua notifikasi untuk user tertentu, diurutkan dari yang terbaru.
    Mengembalikan dalam format standar (data, error, status_code).
    """
    if not user:
        return None, "User tidak ditemukan.", 404
    
    try:
        notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
        return [notif.to_dict() for notif in notifications], None, 200
    except Exception as e:
        return None, f"Terjadi kesalahan saat mengambil notifikasi: {str(e)}", 500

def mark_notification_as_read(user, notification_id):
    """
    Menandai notifikasi sebagai sudah dibaca.
    """
    if not user:
        return None, "User tidak ditemukan.", 404

    try:
        notification = Notification.query.filter_by(id=notification_id, user_id=user.id).first()
        
        if not notification:
            return None, "Notifikasi tidak ditemukan atau bukan milik Anda.", 404
            
        notification.is_read = True
        db.session.commit()
        return notification.to_dict(), "Notifikasi ditandai sebagai dibaca.", 200
    except Exception as e:
        db.session.rollback()
        return None, f"Terjadi kesalahan: {str(e)}", 500