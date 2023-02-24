from flask import Blueprint

eventos = Blueprint('eventos', __name__, url_prefix='/eventos', template_folder='templates')

from . import views