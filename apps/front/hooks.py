from flask import session, g

from config import FRONT_USER_ID
from .models import FrontUser
from .views import front_bp


@front_bp.before_request
def before_request():
    if FRONT_USER_ID in session:
        user_id = session.get(FRONT_USER_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user
