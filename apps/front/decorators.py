from functools import wraps

from flask import session, render_template

from config import FRONT_USER_ID


# 验证登陆装饰器
def login_must(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return render_template('front/login.html')

    return inner
