from flask import Blueprint

diabetes_prediction_bp = Blueprint('diabetes_prediction', __name__)

from . import routes # noqa
