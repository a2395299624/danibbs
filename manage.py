from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps.cms import models as cms_models
from apps.common import models as common_models
from apps.front import models as front_models
from bbs import create_app
from exts import db

CmsUser = cms_models.CmsUser
CmsRole = cms_models.CmsRole
CmsPermission = cms_models.CmsPermission

FrontUser = front_models.FrontUser

Banner = common_models.Banner

app = create_app()
manager = Manager(app)

# 要使用flask_migrate，必须绑定app和db
# compare_type=True 检查字段类型  compare_server_default = True 比较默认值
Migrate(app, db, render_as_batch=True, compare_type=True)
# 把MigrateCommand命令添加到manager中
manager.add_command('db', MigrateCommand)


# 命令既可以用-u,也可以用--username，dest="username"作为参数传给了函数中的username
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
@manager.option('-l', '--level', dest='level')
# 创建cms管理员用户
def create_cms_user(username, password, email, level):
    user = CmsUser(username=username, password=password, email=email, level=level)
    db.session.add(user)
    db.session.commit()
    db.session.rollback()


# 创建权限
@manager.command
def create_role():
    admin = CmsRole(name='管理员', desc='拥有后台管理系统的权限', permission=CmsPermission.ADMIN)
    super_admin = CmsRole(name='管理员', desc='拥有网站的所有权限', permission=CmsPermission.ALL_PERMISSION)

    db.session.add_all([admin, super_admin])
    db.session.commit()


@manager.command
def create_post():
    for x in range(1, 10):
        plate = common_models.Plate().query.first()
        author = FrontUser.query.first()
        post = common_models.Post(title=x, content=x, author=author, plate=plate)
        db.session.add(post)
        db.session.commit()


# 为用户添加权限
@manager.option('-e', '--email', dest='email')
@manager.option('-r', '--role', dest='role')
def user_add_role(email, role):
    user = CmsUser.query.filter_by(email=email).first()
    role = CmsRole.query.filter_by(name=role).first()
    print(user)
    if not user.role:
        role.users.append(user)
    else:
        user.role[0] = role
    db.session.commit()


@manager.command
def test():
    user = FrontUser(telephone='123', password='123', username='123')
    db.session.add(user)
    db.session.commit()


# user = CmsUser.query.filter_by(email='root@qq.com').first()
# user.password = '123'
# db.session.commit()
# print(user.role[0].name)
# if user.has_permission(CmsPermission.CMS_USER_PERMISSION):
#     print("有")
# else:
#     print("没有")


if __name__ == "__main__":
    manager.run()
