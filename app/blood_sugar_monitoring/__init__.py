from flask import Blueprint
blood_sugar_bp = Blueprint('blood_sugar_monitoring', __name__)
from . import routes