# -*- coding:utf-8 -*-

from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
from app_scc.views.view import scc
from app_main.views.view import main


view_list = [scc, main]


def create_app(conf):
    app = Flask(__name__)
    for view in view_list:
        # register static fold path to blueprint
        view.static_folder = conf.static_path
        view.template_folder = conf.template_path(postfix=view.name)
        # register blueprint to app
        app.register_blueprint(view)

    app.config.from_object(conf)
    return app

app = create_app(config['Development'])
db = SQLAlchemy(app)