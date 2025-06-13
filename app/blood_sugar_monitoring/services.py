from app.models.base import db
from app.models.blood_sugar_reading import BloodSugarReading
from datetime import datetime
from app.models.notification import Notification

# --- INI BAGIAN KUNCI INTEGRASI ---
from app.recommendations.services import get_recommendation_service
from app.notifications.services import generate_notification

# --- FUNGSI CREATE YANG SUDAH TERINTEGRASI ---
def add_blood_sugar_service(user, data):
    """
    Menambahkan data pembacaan gula darah baru, mendapatkan rekomendasi,
    dan menyimpan rekomendasi tersebut sebagai notifikasi.
    """

    if not user:
        return False, {"message": "User tidak ditemukan."}, 404

    value = data.get('value')
    notes = data.get('notes')
    condition = data.get('condition')

    if value is None or not condition:
        return False, {"message": "Kadar gula (value) dan kondisi (condition) wajib diisi."}, 400
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        return False, "Nilai gula darah harus berupa angka."
    
    try:
        # Buat entri baru dan kaitkan dengan user.id
        new_reading = BloodSugarReading(
            user_id=user.id,
            value=float(value),
            condition=condition,
            notes=notes,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_reading)
        db.session.commit()

        # --- PANGGIL FITUR LAIN SETELAH DATA DISIMPAN ---
        # 1. Panggil service Rekomendasi
        # recommendation_text = get_recommendation_service(
        #     value, # Menggunakan 'value'
        #     meal_condition=new_reading.condition # Menggunakan 'meal_condition' sesuai definisi fungsi di bawah
        # )
        recommendation_text = get_recommendation_service(
            user.profile.age, # Ambil data profil user
            value, 
            condition,
            user.profile.precondition # misal: 'sehat', 'pradiabetes'
        )
        
        if recommendation_text:
            # Buat objek Notifikasi baru dari teks rekomendasi
            new_notification = Notification(
                user_id=user.id,
                message=f"Rekomendasi: {recommendation_text}"
            )
            db.session.add(new_notification)
            db.session.commit()

        # 2. Panggil service Notifikasi
        notification_message = generate_notification(user.profile.age, # Ambil data profil user
            value, 
            condition,
            user.profile.precondition)

        # 3. Siapkan response yang kaya akan informasi
        response_data = {
            "message": "Data gula darah berhasil disimpan.",
            "reading": new_reading.to_dict(), # Asumsi ada method to_dict() di model
            "recommendation": recommendation_text,
            "notification": notification_message
        }
        return True, response_data, 200
    
    except Exception as e:
        db.session.rollback()
        return False, {"message": f"An unexpected error occurred: {str(e)}"}, 500

# --- FUNGSI READ DENGAN FILTER USER ---
def get_all_readings_service(user):
    """
    Mengambil semua riwayat pembacaan gula darah untuk seorang user,
    dan mengembalikan dalam format (data, error, status_code).
    """
    if not user:
        return None, "User tidak ditemukan.", 404
    
    try:
        readings = BloodSugarReading.query.filter_by(user_id=user.id).order_by(BloodSugarReading.timestamp.desc()).all()
        # Jika berhasil, kembalikan 3 nilai: data, None untuk error, dan 200 untuk status
        return [reading.to_dict() for reading in readings], None, 200
    except Exception as e:
        # Jika ada error database, kembalikan 3 nilai: None, pesan error, dan 500
        return None, f"An unexpected error occurred: {str(e)}", 500

def get_user_readings_service(user):
    # .query.filter_by(user_id=user.id) adalah kuncinya!
    readings = BloodSugarReading.query.filter_by(user_id=user.id).order_by(BloodSugarReading.timestamp.desc()).all()
    return [r.to_dict() for r in readings]

def get_reading_by_id_service(user, reading_id):
    # Filter berdasarkan ID DAN user_id untuk keamanan
    reading = BloodSugarReading.query.filter_by(id=reading_id, user_id=user.id).first()
    return reading.to_dict() if reading else None

# --- FUNGSI UPDATE & DELETE DENGAN OTORISASI ---
def update_reading_service(user, reading_id, data):
    # Cari reading yang spesifik milik user ini
    reading = BloodSugarReading.query.filter_by(id=reading_id, user_id=user.id).first()
    
    if not reading:
        return False, "Data tidak ditemukan atau Anda tidak memiliki akses."

    # Lakukan update
    new_value = data.get('value')
    if new_value is not None:
        try:
            reading.value = float(new_value)
        except (ValueError, TypeError):
            return False, "Nilai gula darah harus berupa angka."
    reading.notes = data.get('notes', reading.notes)
    
    db.session.commit()
    return True, "Data berhasil diupdate."

def delete_reading_service(user, reading_id):
    reading = BloodSugarReading.query.filter_by(id=reading_id, user_id=user.id).first()
    
    if not reading:
        return False, "Data tidak ditemukan atau Anda tidak memiliki akses."
        
    db.session.delete(reading)
    db.session.commit()
    return True, "Data berhasil dihapus."