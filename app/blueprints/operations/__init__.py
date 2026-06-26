from flask import Blueprint

bp = Blueprint('operations', __name__, template_folder='templates')

from . import routes
