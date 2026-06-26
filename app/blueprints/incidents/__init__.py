from flask import Blueprint

incidents_bp = Blueprint('incidents', __name__, template_folder='templates')

from . import routes
