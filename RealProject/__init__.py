import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from RealProject.settings import BASE_PATH


db = SQLAlchemy()
migrate = Migrate()

# 初始化Flask 框架 , 利用工厂函数

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the test config if passed in
        CONFIG_PATH = BASE_PATH / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    
    else:
        # load the instance config, if it exists, when not testing
        app.config.from_mapping(test_config)

    # 初始化数据库

    db.init_app(app)
    migrate.init_app(app, db)


    # 注册蓝图
    from app import auth, blog
    from app.blog import views as blog_views
    from app.auth import views as auth_views
    from app.admin import views as admin_views
    # app.register_blueprint(auth.bp)
    app.register_blueprint(blog_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(admin_views.bp)
    
    app.add_url_rule('/', endpoint='index', view_func=blog_views.index)
    
    # 注册数据库
    
    from app.blog import models
    from app.auth import models


    

    # # 注册过滤器
    # from . import filters
    # app.add_template_filter(filters.format_datetime)

    # # 注册命令
    # from . import commands
    # app.cli.add_command(commands.init_db_command)

    return app