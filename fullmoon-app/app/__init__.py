# -*- coding:utf-8 -*-

from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
from app_scc.views.view import scc
from app_main.views.view import main


def create_app(conf):
    app = Flask(__name__)
    # 注册静态文件地址
    scc.static_folder = conf.static_path
    main.static_folder = conf.static_path
    # 注册蓝图
    app.register_blueprint(scc)
    app.register_blueprint(main)
    app.config.from_object(conf)
    return app

app = create_app(config['Development'])
db = SQLAlchemy(app)