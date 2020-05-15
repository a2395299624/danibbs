import ast

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send_sms(telephone, **code):
    client = AcsClient('LTAI4GDYb2ZKzHEsSkKzqQkq', 'pMERJqMMxAJp8hxflOVIhhN0pH1gUs', 'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('SignName', "达尼论坛")
    request.add_query_param('TemplateCode', "SMS_189245302")
    request.add_query_param('PhoneNumbers', telephone)
    request.add_query_param('TemplateParam', code)

    response = client.do_action_with_exception(request)

    # print('短信信息：' + (str(response, encoding='utf-8')))

    return ast.literal_eval(str(response, encoding='utf-8'))
