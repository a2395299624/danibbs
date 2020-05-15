from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, abort
from flask_paginate import Pagination, get_parameter
from sqlalchemy import func

from config import FRONT_USER_ID
from exts import db
from tools import restful, memcache
from .decorators import login_must
from .models import FrontUser
from ..common.models import Banner, Plate, Post, Comment

front_bp = Blueprint("front", __name__, )


@front_bp.route('/')
def index():
    banners = Banner.query.order_by(Banner.priority.desc()).limit(4)
    plates = Plate().query.all()
    posts_top = Post.query.filter(Post.top.is_(True))
    page = request.args.get(get_parameter('p'), type=int, default=1)
    plate_id = request.args.get('plate', type=int, default=None)
    sort = request.args.get('sort', type=str, default="new")
    start = (page - 1) * 10
    end = start + 10
    query_obj = Post.query
    if sort == "new":
        query_obj = Post.query.order_by(Post.create_time.desc())
    elif sort == 'hot':
        query_obj = Post.query.order_by(Post.read_num.desc())
    elif sort == 'like':
        pass
    elif sort == 'reply':
        query_obj = db.session.query(Post).outerjoin(Comment).group_by(Post.id).order_by(func.count(Comment.id).desc())
    if plate_id:
        query = query_obj.filter(Post.plate_id == plate_id)
        posts = query.slice(start, end)
        total = query.count()
    else:
        query = query_obj.filter(Post.recommend.is_(True))
        posts = query.slice(start, end)
        total = query.count()
    pagination = Pagination(page_parameter="p", bs_version=3, p=page, total=total, outer_window=0)
    context = {
        "banners": banners,
        "plates": plates,
        "posts": posts,
        "posts_top": posts_top,
        "pagination": pagination,
        'select_plate': plate_id,
        'select_sort': sort,
    }
    return render_template('front/index.html', **context)


@front_bp.route('/post/', methods=['GET', 'POST'])
@login_must
def post():
    if request.method == 'GET':
        plates = Plate.query.all()
        return render_template('front/post.html', plates=plates)

    if request.method == 'POST':
        title = request.form.get("title")
        text = request.form.get("text")
        plate_id = request.form.get("plate_id")
        plate = Plate.query.get(plate_id)
        if plate:
            plate.post_num = plate.post_num + 1
            post = Post(title=title, content=text)
            post.author = g.front_user
            post.plate = plate
            db.session.add(post)
            db.session.commit()
            url_go = url_for('front.details', post_id=post.id)
            return restful.success(data={"url_go": url_go})
        return restful.params_error('没有这个板块')


@front_bp.route('/details/<post_id>/')
def details(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    post.read_num = post.read_num + 1
    db.session.commit()
    return render_template('front/details.html', post=post)


@front_bp.route('/comment/', methods=['POST'])
@login_must
def comment():
    content = request.form.get('content')
    post_id = request.form.get('post_id')
    post = Post.query.get(post_id)
    if post:
        comment = Comment(content=content)
        comment.post = post
        comment.author = g.front_user
        db.session.add(comment)
        db.session.commit()
        return restful.success()
    return restful.params_error('该帖子不存在')


class RegisterView(views.MethodView):
    def get(self):
        return render_template('front/register.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        telephone = request.form.get('telephone')
        smscaptcha = request.form.get('smscaptcha')
        user = FrontUser.query.filter_by(username=username).first()

        if not user:
            memcached_captcha = memcache.get(telephone)
            if not memcached_captcha or smscaptcha != memcached_captcha:
                return restful.unauth_error('短信验证码错误')
            else:
                newuser = FrontUser(telephone=telephone, password=password, username=username)
                db.session.add(newuser)
                db.session.commit()
                return restful.success()
        else:
            return restful.params_error('昵称已被使用')


class LoginView(views.MethodView):
    def get(self):
        url_go = request.referrer
        act = request.args.get('act')
        if act == 'exit':
            del session[FRONT_USER_ID]
            return render_template('common/exit.html', url_go=url_go)
        if FRONT_USER_ID in session:
            return redirect('/')
        return render_template('front/login.html', url_go=url_go)

    def post(self):
        username = request.form.get('username')
        telephone = request.form.get('telephone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        remember = request.form.get('remember')
        if telephone:
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password1):
                session[FRONT_USER_ID] = user.id
                if remember:
                    # 开启session过期时间
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error()
        if username:
            user = FrontUser.query.filter_by(username=username).first()
            if user and user.check_password(password2):
                session[FRONT_USER_ID] = user.id
                if remember:
                    # 开启session过期时间
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error()
        return restful.unauth_error()


front_bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
front_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
