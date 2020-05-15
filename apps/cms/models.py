from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from exts import db


class CmsPermission(object):
    ALL_PERMISSION = 0b11111111
    # 管理员
    ADMIN = 0b00011111

    # 访问权限
    VISITOR_PERMISSION = 0b00000001

    # 帖子权限
    POST_PERMISSION = 0b00000010

    # 评论权限
    COMMENT_PERMISSION = 0b00000100

    # 板块权限
    PLATE_PERMISSION = 0b00001000

    # 网站用户权限
    WEB_USER_PERMISSION = 0b00010000

    # 后台用户权限
    CMS_USER_PERMISSION = 0b00100000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


class CmsRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    desc = db.Column(db.String(50), nullable=False)
    permission = db.Column(db.Integer, nullable=False, default=CmsPermission.ADMIN)

    users = db.relationship('CmsUser', secondary=cms_role_user, backref='role')


class CmsUser(db.Model):
    __tablename__ = "cms_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now())

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, value):
        result = check_password_hash(self.password, value)
        return result

    @property
    def permission(self):
        if not self.role:
            return 0
        all_permission = 0
        for role in self.role:
            permissions = role.permission
            all_permission |= permissions
        return all_permission

    def has_permission(self, permission):
        return self.permission & permission == permission

