from flask import Blueprint

bp = Blueprint('teams', __name__, template_folder='templates')

from . import routes
