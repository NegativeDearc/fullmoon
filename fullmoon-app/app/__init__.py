# -*- coding:utf-8 -*-

from flask import Flask, request, session, abort
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os

db = SQLAlchemy()
lm = LoginManager()


def create_app(conf):
    #
    from views.scc_view import scc
    from views.main_view import main
    view_list = [scc, main]

    app = Flask(__name__)

    for view in view_list:
        # register static fold path to blueprint
        view.static_folder = conf.static_path
        view.template_folder = conf.template_path(postfix=view.name)
        # register blueprint to app
        app.register_blueprint(view)
    app.config.from_object(conf)
    # to apply config to sqlalchemy, must init after app applied config
    db.init_app(app)
    lm.init_app(app)
    return app


def csrf_protect():
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_crsf_token'):
            abort(403)


def generate_csrf_token():
    if '_crsf_token' not in session:
        session['_crsf_token'] = os.urandom(30).encode('hex')
    return session['_crsf_token']


app = create_app(config['development'])
app.jinja_env.globals['crsf_token'] = generate_csrf_token

if not app.debug:
    print True
    # in production,logs must be recorded
    # from app.logs.log import DebugFalseLog
    #
    # handler = DebugFalseLog().get_handler()
    # app.logger.addHandler(handler)
    pass
