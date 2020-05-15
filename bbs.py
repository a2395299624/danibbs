from datetime import datetime

from flask import Flask, render_template
from flask_wtf import CSRFProtect

import config
from apps.cms import cms_bp
from apps.common import common_bp
from apps.front import front_bp
from apps.ueditor import ueditor_bp
from exts import db, mail


def create_app():
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(config)

    # 注册蓝图
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)

    # 绑定SQLAlchemy
    db.init_app(app)
    # 绑定CSRF保护
    CSRFProtect(app)
    # 绑定mail
    mail.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('common/error_404.html')

    @app.template_filter("time_filter")
    def time_filter(time):
        now = datetime.now()
        period = (now - time).total_seconds()
        if period < 180:
            return "刚刚"
        elif 180 <= period < 3600:
            return "%s分钟前" % int(period / 60)
        elif 3600 <= period < 86400:
            return "%s小时前" % int(period / 3600)
        elif 86400 <= period < 2592000:
            return "%s天前" % int(period / 86400)
        else:
            return time.strftime('%Y-%m-%d')

    @app.template_filter("time_simple")
    def time_simple(time):
        return time.strftime('%Y-%m-%d')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
