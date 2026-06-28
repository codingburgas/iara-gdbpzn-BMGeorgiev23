from flask import Blueprint

operations_bp = Blueprint('operations', __name__, template_folder='templates')

from . import routes