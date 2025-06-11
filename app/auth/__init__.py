# app/auth/__init__.py (KODE YANG BENAR)

from flask import Blueprint

# Hanya definisikan Blueprint di sini
auth_bp = Blueprint('auth', __name__)

# Impor routes agar semua endpoint di dalamnya terdaftar ke blueprint ini
from . import routes