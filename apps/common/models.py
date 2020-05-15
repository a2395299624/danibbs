from datetime import datetime

from exts import db


class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=0)


class Plate(db.Model):
    __tablename__ = 'plate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    post_num = db.Column(db.Integer, nullable=False, default=0)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    top = db.Column(db.Boolean, default=False)
    recommend = db.Column(db.Boolean, default=False)
    read_num = db.Column(db.Integer, default=0)
    plate_id = db.Column(db.Integer, db.ForeignKey('plate.id'), nullable=False)
    author_id = db.Column(db.String(50), db.ForeignKey("front_user.id"), nullable=False)

    plate = db.relationship('Plate', backref='posts')
    author = db.relationship("FrontUser", backref='posts')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.String(50), db.ForeignKey("front_user.id"), nullable=False)

    author = db.relationship("FrontUser", backref='comments')
    post = db.relationship("Post", backref='comments')
