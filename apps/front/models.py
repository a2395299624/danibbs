import enum
from datetime import datetime

import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db


class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class FrontUser(db.Model):
    __tablename__ = "front_user"
    id = db.Column(db.String(50), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    signature = db.Column(db.String(50))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    register_time = db.Column(db.DateTime, default=datetime.now())

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, value):
        result = check_password_hash(self.password, value)
        return result
