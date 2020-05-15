import random
import string

from flask import Blueprint, views, render_template, request, session, redirect, url_for, flash, g
from flask_paginate import Pagination, get_parameter

from config import CMS_USER_ID
from exts import db
from tasks import send_mail
from tools import restful, memcache
from .decorators import login_must, permission_must
from .forms import ResetEmailForm
from .models import CmsUser, CmsPermission
from ..common.models import Banner, Plate, Post, Comment

cms_bp = Blueprint("cms", __name__, url_prefix="/cms")


# 首页
@cms_bp.route('/index/')
@login_must
def index():
    return render_template('cms/cms_index.html')


# 个人中心
@cms_bp.route('/profile/')
@login_must
def profile():
    return render_template("cms/cms_profile.html")


# 轮播图
@cms_bp.route('/banners/')
@login_must
def banners():
    banners = Banner().query.all()
    return render_template("cms/cms_banners.html", banners=banners)


# 添加轮播图
@cms_bp.route('/abanner/', methods=['POST'])
@login_must
def abanner():
    name = request.form.get('name')
    image = request.form.get('image')
    url = request.form.get('url')
    priority = request.form.get('priority')
    banner = Banner(name=name, image=image, url=url, priority=priority)
    db.session.add(banner)
    db.session.commit()
    return restful.success()


# 修改轮播图
@cms_bp.route('/ubanner/', methods=['POST'])
@login_must
def ubanner():
    name = request.form.get('name')
    image = request.form.get('image')
    url = request.form.get('url')
    priority = request.form.get('priority')
    banner_id = request.form.get('id')
    banner = Banner.query.get(banner_id)
    if banner:
        banner.name = name
        banner.image = image
        banner.url = url
        banner.priority = priority
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error('轮播图不存在')


# 删除轮播图
@cms_bp.route('/dbanner/', methods=['POST'])
@login_must
def dbanner():
    banner_id = request.form.get('id')
    banner = Banner.query.get(banner_id)
    if banner:
        db.session.delete(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error('轮播图不存在')


# 帖子
@cms_bp.route('/post/')
@login_must
def post():
    page = request.args.get(get_parameter('p'), type=int, default=1)
    start = (page - 1) * 10
    end = start + 10
    total = Post.query.count()
    posts = Post.query.order_by(Post.create_time.asc()).slice(start, end)
    pagination = Pagination(page_parameter="p", p=page, bs_version=3, total=total, outer_window=0)
    return render_template("cms/cms_post.html", posts=posts, pagination=pagination)


@cms_bp.route('/dpost/', methods=['POST'])
@login_must
def dpost():
    post_id = request.form.get('id')
    if not post_id:
        return restful.params_error('请传入帖子ID')
    post = Post.query.get(post_id)
    if post:
        for comment in post.comments:
            db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
        return restful.success()
    return restful.params_error('该帖子不存在')


@cms_bp.route('/tpost/', methods=['POST'])
@login_must
def hpost():
    post_id = request.form.get('id')
    if not post_id:
        return restful.params_error('请传入帖子ID')
    post = Post.query.get(post_id)
    if post:
        post.top = True
        db.session.commit()
        return restful.success()
    return restful.params_error('该帖子不存在')


@cms_bp.route('/notpost/', methods=['POST'])
@login_must
def nohpost():
    post_id = request.form.get('id')
    if not post_id:
        return restful.params_error('请传入帖子ID')
    post = Post.query.get(post_id)
    if post:
        post.top = False
        db.session.commit()
        return restful.success()
    return restful.params_error('该帖子不存在')


@cms_bp.route('/rpost/', methods=['POST'])
@login_must
def rpost():
    post_id = request.form.get('id')
    if not post_id:
        return restful.params_error('请传入帖子ID')
    post = Post.query.get(post_id)
    if post:
        post.recommend = True
        db.session.commit()
        return restful.success()
    return restful.params_error('该帖子不存在')


@cms_bp.route('/norpost/', methods=['POST'])
@login_must
def norpost():
    post_id = request.form.get('id')
    if not post_id:
        return restful.params_error('请传入帖子ID')
    post = Post.query.get(post_id)
    if post:
        post.recommend = False
        db.session.commit()
        return restful.success()
    return restful.params_error('该帖子不存在')


# 评论
@cms_bp.route('/comment/', methods=['POST', 'GET'])
@login_must
def comment():
    if request.method == 'POST':
        comment_id = request.form.get('id')
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('这条评论不存在')

    if request.method == 'GET':
        page = request.args.get(get_parameter('p'), type=int, default=1)
        start = (page - 1) * 10
        end = start + 10
        total = Comment.query.count()
        comments = Comment.query.slice(start, end)
        pagination = Pagination(page_parameter="p", p=page, bs_version=3, total=total, outer_window=0)
        return render_template("cms/cms_comment.html", comments=comments, pagination=pagination)


# 板块
@cms_bp.route('/plate/')
@login_must
def plate():
    plates = Plate().query.all()
    return render_template("cms/cms_plate.html", plates=plates)


@cms_bp.route('/aplate/', methods=['POST'])
@login_must
def aplate():
    name = request.form.get('name')
    plate_ = Plate(name=name)
    db.session.add(plate_)
    db.session.commit()
    return restful.success()


@cms_bp.route('/uplate/', methods=['POST'])
@login_must
def uplate():
    plate_id = request.form.get('id')
    plate_name = request.form.get('name')
    plate_ = Plate.query.get(plate_id)
    if plate_:
        plate_.name = plate_name
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error("该板块不存在")


@cms_bp.route('/dplate/', methods=['POST'])
@login_must
def dplate():
    plate_id = request.form.get('id')
    plate_ = Plate.query.get(plate_id)
    if plate_:
        db.session.delete(plate_)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error('该板块不存在')


# 用户
@cms_bp.route('/webuser/')
@login_must
def webuser():
    return render_template("cms/cms_webuser.html")


# cms用户
@cms_bp.route('/cmsuser/')
@login_must
@permission_must(CmsPermission.CMS_USER_PERMISSION)
def cmsuser():
    return render_template("cms/cms_cmsuser.html")


# cms组
@cms_bp.route('/cmsgroup/')
@login_must
@permission_must(CmsPermission.CMS_USER_PERMISSION)
def cmsgroup():
    return render_template("cms/cms_cmsgroup.html")


# 注销
@cms_bp.route('/logout/')
def logout():
    if CMS_USER_ID in session:
        del session[CMS_USER_ID]
        flash("成功注销", "logout")
        return redirect(url_for("cms.login"))
    else:
        flash("成功注销", "logout")
        return redirect(url_for("cms.login"))


# 修改密码视图类
class ResetPwd(views.MethodView):
    decorators = [login_must]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        newpwd = request.form.get('newpwd')
        oldpwd = request.form.get('oldpwd')
        user = g.cms_user
        if user.check_password(oldpwd):
            user.password = newpwd
            db.session.commit()
            return restful.success("密码修改成功!", )
        else:
            return restful.params_error("旧密码错误")


# 发送邮箱验证码
@cms_bp.route('/emailcaptcha/')
def email_captcha():
    email = request.args.get('email')
    captcha = list(string.ascii_letters)
    captcha.extend(map(lambda x: str(x), range(0, 10)))
    captcha = ''.join(random.sample(captcha, 6))
    user = g.cms_user
    try:
        send_mail.delay("达尼论坛验证码", [email], captcha, user.username, '更改邮箱')
        memcache.set(email, captcha)
    except:
        return restful.params_error('此邮箱不存在')
    return restful.success()


# 修改邮箱视图类
class ResetEmail(views.MethodView):
    decorators = [login_must]

    def get(self):
        return render_template("cms/cms_resetemail.html")

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


# 登录视图类
class LoginView(views.MethodView):
    def get(self, ):
        if CMS_USER_ID in session:
            return redirect(url_for('cms.index'))
        else:
            return render_template('cms/cms_login.html', )

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = CmsUser.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session[CMS_USER_ID] = user.id
            if remember:
                # 开启session过期时间
                session.permanent = True
            return redirect(url_for('cms.index'))
        else:
            # 设置消息闪现
            flash("!邮箱或密码错误", "login")
            return redirect(url_for("cms.login"))


cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
cms_bp.add_url_rule('/resetpwd/', view_func=ResetPwd.as_view('resetpwd'))
cms_bp.add_url_rule('/resetemail/', view_func=ResetEmail.as_view('resetemail'))
