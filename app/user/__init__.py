from flask import Blueprint

user = Blueprint('user', __name__)

from . import views


@user.app_context_processor
def inject_int():
    return dict(int=int)