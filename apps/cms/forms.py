from flask import g
from wtforms import Form, StringField, ValidationError
from wtforms.validators import DataRequired

from tools import memcache


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class ResetEmailForm(BaseForm):
    email = StringField(validators=[])
    captcha = StringField(validators=[DataRequired()])

    def validate_captcha(self, field):
        captcha = self.captcha.data
        email = self.email.data
        memcached_captcha = memcache.get(email)
        if memcached_captcha is None:
            raise ValidationError("验证码错误!")
        if not memcached_captcha or captcha.lower() != memcached_captcha.lower():
            raise ValidationError("验证码错误!")

    def validate_email(self, field):
        email = self.email.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("不能修改为相同邮箱")
