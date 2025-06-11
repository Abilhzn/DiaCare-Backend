# app/blood_sugar_monitoring/services.py (KODE LENGKAP YANG DIPERBAIKI)

from app.models.base import db
from app.models.blood_sugar_reading import BloodSugarReading # Pastikan model ini ada
from datetime import datetime

# --- INI BAGIAN KUNCI INTEGRASI ---
# Impor service dari fitur lain
from app.recommendations.services import get_recommendations_for_reading # Asumsi nama fungsinya ini
from app.notifications.services import create_sugar_alert_notification # Asumsi nama fungsinya ini

# --- FUNGSI CREATE YANG SUDAH TERINTEGRASI ---
def add_blood_sugar_service(user, data):
    value = data.get('value')
    notes = data.get('notes')
    # Tambahan: Ambil kondisi makan dari input
    condition = data.get('condition') # misal: 'sebelum_makan' atau 'setelah_makan'

    if value is None:
        return False, "Nilai gula darah tidak boleh kosong."
    
    try:
        float_value = float(value)
    except (ValueError, TypeError):
        return False, "Nilai gula darah harus berupa angka."

    # Buat entri baru dan kaitkan dengan user.id
    new_reading = BloodSugarReading(
        value=float_value,
        notes=notes,
        user_id=user.id,
        timestamp=datetime.utcnow(),
        condition=condition
    )
    db.session.add(new_reading)
    db.session.commit()

    # --- PANGGIL FITUR LAIN SETELAH DATA DISIMPAN ---
    # 1. Panggil service Rekomendasi
    recommendation_text = get_recommendations_for_reading(
        sugar_level_value=new_reading.value, 
        user_age=user.profile.age, # Ambil data profil user
        user_category=user.profile.precondition, # misal: 'sehat', 'pradiabetes'
        meal_condition=new_reading.condition
    )
    
    # 2. Panggil service Notifikasi
    notification_message = create_sugar_alert_notification(user, new_reading.value)

    # 3. Siapkan response yang kaya akan informasi
    response_data = {
        "message": "Data gula darah berhasil disimpan.",
        "reading": new_reading.to_dict(), # Asumsi ada method to_dict() di model
        "recommendation": recommendation_text,
        "notification": notification_message
    }
    
    return True, response_data

# --- FUNGSI READ DENGAN FILTER USER ---
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
    return True, "Data berhasil dihapus."from app.models.base import db
from app.models.blood_sugar_reading import BloodSugarReading # Pastikan model ini ada
from datetime import datetime

# --- INI BAGIAN KUNCI INTEGRASI ---
# Impor service dari fitur lain
from app.recommendations.services import get_recommendations_for_reading # Asumsi nama fungsinya ini
from app.notifications.services import create_sugar_alert_notification # Asumsi nama fungsinya ini

# --- FUNGSI CREATE YANG SUDAH TERINTEGRASI ---
def add_blood_sugar_service(user, data):
    value = data.get('value')
    notes = data.get('notes')
    # Tambahan: Ambil kondisi makan dari input
    condition = data.get('condition') # misal: 'sebelum_makan' atau 'setelah_makan'

    if value is None:
        return False, "Nilai gula darah tidak boleh kosong."
    
    try:
        float_value = float(value)
    except (ValueError, TypeError):
        return False, "Nilai gula darah harus berupa angka."

    # Buat entri baru dan kaitkan dengan user.id
    new_reading = BloodSugarReading(
        value=float_value,
        notes=notes,
        user_id=user.id,
        timestamp=datetime.utcnow(),
        condition=condition
    )
    db.session.add(new_reading)
    db.session.commit()

    # --- PANGGIL FITUR LAIN SETELAH DATA DISIMPAN ---
    # 1. Panggil service Rekomendasi
    recommendation_text = get_recommendations_for_reading(
        sugar_level_value=new_reading.value, 
        user_age=user.profile.age, # Ambil data profil user
        user_category=user.profile.precondition, # misal: 'sehat', 'pradiabetes'
        meal_condition=new_reading.condition
    )
    
    # 2. Panggil service Notifikasi
    notification_message = create_sugar_alert_notification(user, new_reading.value)

    # 3. Siapkan response yang kaya akan informasi
    response_data = {
        "message": "Data gula darah berhasil disimpan.",
        "reading": new_reading.to_dict(), # Asumsi ada method to_dict() di model
        "recommendation": recommendation_text,
        "notification": notification_message
    }
    
    return True, response_data

# --- FUNGSI READ DENGAN FILTER USER ---
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