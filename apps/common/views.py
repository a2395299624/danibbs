import random
import string
from io import BytesIO

import qiniu
from flask import Blueprint, request, make_response, jsonify

from tools import aliyunsdk, restful, yprequest, memcache
from tools.captcha import Captcha
from ..front.models import FrontUser
from tasks import send_sms_captcha

common_bp = Blueprint("common", __name__, url_prefix="/common")


# 手机验证码
@common_bp.route('/sms/', methods=['POST'])
def send_sms():
    telephone = request.form.get('telephone')
    token = request.form.get("token")
    authenticate = request.form.get("authenticate")
    check_ret = yprequest.check_ticket(token, authenticate)
    user = FrontUser.query.filter_by(telephone=telephone).first()
    if not user:
        if check_ret.get("code") == 0:
            captcha = ''.join(random.sample(list(string.digits), 6))
            result = send_sms_captcha(telephone, captcha)
            memcache.set(telephone, captcha, timeout=300)
            if result.get('Code') == 'OK':
                return restful.success()
            else:
                return restful.unauth_error()
        else:
            return restful.server_error()
    return restful.params_error()


# 图形验证码
@common_bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@common_bp.route('/uptoken/')
def uptoken():
    access_key = 'o4FRYaXOdV54Tok_yjD01AsSrGcRTEClCuxIsPro'
    secret_key = 'UOX3tkgoZ0f7cZL8DXJUjrsa0UkwjX_KRRsUk1jk'
    q = qiniu.Auth(access_key, secret_key)
    bucket_name = 'danibbs'
    token = q.upload_token(bucket_name)
    return jsonify({"uptoken": token})
