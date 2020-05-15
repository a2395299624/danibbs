import ast
import hashlib
import random
import time

import requests


def check_ticket(token, authenticate):
    data = {
        'authenticate': authenticate,
        'captchaId': "e452fd6b22734687aa5698511b0c8852",
        'nonce': str(random.randint(10000, 99999)),
        'secretId': "75081d011a0b4a6d80d78ab38339db64",
        'timestamp': str(time.time()).split('.')[0],
        'token': token,
        'version': '1.0'
    }
    sign_str = ''
    items = sorted(data.items(), key=lambda d: d[0])

    for item in items:
        sign_str += '%s%s' % (item[0], item[1])

    sign_str += "2a21cbf3eca24acbb8c5b79404899682"

    signature = hashlib.md5(sign_str.encode("utf8")).hexdigest().lower()
    data['signature'] = signature
    url = 'https://captcha.yunpian.com/v1/api/authenticate'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(url, data=data, headers=headers)
    return ast.literal_eval(r.text)
