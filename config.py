import os
from datetime import timedelta

DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)

# 数据库服务器配置
DB_USERNAME = "root"
DB_PASSWORD = "liyulong123"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = 'bbs论坛'
DB_URL = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

# 邮箱服务器配置
# MAIL_USE_TLS:端口号587
# MAIL_USE_SSL:端口号465

MAIL_SERVER = "smtp.exmail.qq.com"
MAIL_PORT = "465"
# MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = "danibbs@lylweb.xyz"
MAIL_PASSWORD = "Lyl888"
MAIL_DEFAULT_SENDER = "达尼论坛<danibbs@lylweb.xyz>"

# 设置session过期时间为1天
PERMANENT_SESSION_LIFETIME = timedelta(days=3)
# 设置session名称
SESSION_COOKIE_NAME = "moon_bbs"

# 指定SECRET_KEY 盐加密
SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

compare_type = True
compare_server_default = True

# 常量
CMS_USER_ID = "jwkflwejoif"
FRONT_USER_ID = 'bfgjoijewoigfweqwdqw'

# UEditor配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "o4FRYaXOdV54Tok_yjD01AsSrGcRTEClCuxIsPro"
UEDITOR_QINIU_SECRET_KEY = "UOX3tkgoZ0f7cZL8DXJUjrsa0UkwjX_KRRsUk1jk"
UEDITOR_QINIU_BUCKET_NAME = "danibbs"
UEDITOR_QINIU_DOMAIN = "http://q9xc69071.bkt.clouddn.com/"

CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
