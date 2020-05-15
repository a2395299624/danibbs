from flask import session, g

from config import CMS_USER_ID
from .models import CmsUser, CmsPermission
from .views import cms_bp


@cms_bp.before_request
def before_request():
    if CMS_USER_ID in session:
        user_id = session.get(CMS_USER_ID)
        user = CmsUser.query.get(user_id)
        if user:
            g.cms_user = user


@cms_bp.context_processor
def cms_context_processor():
    return {'CmsPermission': CmsPermission}
