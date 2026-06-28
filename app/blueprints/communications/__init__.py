from flask import Blueprint

communications_bp = Blueprint('communications', __name__, template_folder='templates')

from . import routes