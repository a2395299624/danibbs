from functools import wraps

from flask import session, redirect, url_for, g

from config import CMS_USER_ID


# 验证登陆装饰器
def login_must(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))

    return inner


# 验证权限装饰器
def permission_must(permission):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for("cms.index"))

        return inner

    return outer
