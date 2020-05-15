from celery import Celery
from flask import render_template, Flask
from flask_mail import Message

import config
from exts import mail
from tools.aliyunsdk import send_sms

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def send_mail(subject, recipients, captcha, username, operate):
    message = Message(subject, recipients)
    message.html = render_template('common/sendemail.html', captcha=captcha, username=username, operate=operate)
    mail.send(message)


@celery.task
def send_sms_captcha(telephone, captcha):
    return send_sms(telephone, code=captcha)
