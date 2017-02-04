# -*- coding:utf-8 -*-
from flask import Flask, request, session, abort, g
from config import config
from flask.ext.login import LoginManager
from flask.ext.httpauth import HTTPBasicAuth
import os
from models.database import db, mail
from models.model import Login
from uuid import uuid1
from flask.ext.restful import Api
from bs4 import BeautifulSoup
import urllib
import hashlib
import re

lm = LoginManager()
auth = HTTPBasicAuth()


def create_app(conf):
    from views.scc_view import scc
    from views.main_view import main
    from views.cxw_view import cxw
    # from views.api_view import api
    # view_list = [scc, main, api]
    view_list = [scc, main, cxw]

    app = Flask(__name__)
    # to apply config to app,must before init of SQLAlchemy and LoginManager
    app.config.from_object(conf)
    #
    from app.views.api_view import ToolsApi, ArticleApi, ApiRoute, ApiComment
    api = Api(app)
    api.add_resource(ToolsApi, '/api/tools/uuid/', endpoint='tool')
    api.add_resource(ArticleApi, '/api/article/uuid/<uuid>', endpoint='article')
    api.add_resource(ApiComment, '/api/comment/id/<id>', endpoint='comment')
    api.add_resource(ApiRoute, '/api/token/', endpoint='route')

    db.init_app(app)
    # http://blog.csdn.net/yannanxiu/article/details/53426359
    # http://www.pythondoc.com/flask-sqlalchemy/api.html#flask.ext.sqlalchemy.SQLAlchemy.init_app
    # http://librelist.com/browser/flask/2010/8/30/sqlalchemy-init-app-problem/
    db.app = app
    # do not use setup_app()
    lm.session_protection = 'strong'
    lm.login_view = "main.main_login"
    lm.refresh_view = "main.main_login"
    lm.needs_refresh_message = u"To protect your account, please re-authenticate to access this page."
    lm.needs_refresh_message_category = "info"

    # lm callback
    @lm.user_loader
    def load_user(uid):
        return Login.get(uid)

    # auth callback
    @auth.verify_password
    def verify_password(username_or_token, password):
        user = Login.verify_auth_token(username_or_token)
        if not user:
            user = Login.query.filter_by(user=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user_ = user  # distinguish with flask-login user
        return True

    lm.init_app(app)
    mail.init_app(app)

    for view in view_list:
        # register static fold path to blueprint
        view.static_folder = conf.static_path
        view.template_folder = conf.template_path(postfix=view.name)
        # register blueprint to app
        app.register_blueprint(view)
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


def generate_uuid():
    return uuid1().__str__()


# remove all tags of html for use instead of safe filter
def sanitize_html(value):
    soup = BeautifulSoup(value, "html.parser")
    for tag in soup.findAll(True):
        tag.hidden = True
    soup = unicode(soup)
    return soup


# todo: use re to remove all blank/tab/white space at html
def remove_blank(value):
    pass


# use gravatar generate avatar by email
def gravatar_url(email, size=40):
    # just pass one of the following keywords as the d= parameter to an image request:
    # 404: do not load any image if none is associated with the email hash,instead return an 404 response
    # mm: (mystery-man) a simple, cartoon-style silhouetted outline of a person (does not vary by email hash)
    # identicon: a geometric pattern based on an email hash
    # monsterid: a generated 'monster' with different colors, faces, etc
    # wavatar: generated faces with differing features and backgrounds
    # retro: awesome generated, 8-bit arcade-style pixelated faces
    # blank: a transparent PNG image (border added to HTML below for demonstration purposes)
    gravatar = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar += urllib.urlencode({'s': str(size), 'd': "monsterid"})
    return gravatar


def jinja_length(element):
    if hasattr(element, '__len__'):
        return len(element)


app = create_app(config['development'])
app.jinja_env.globals['crsf_token'] = generate_csrf_token
app.jinja_env.globals['uuid'] = generate_uuid
app.jinja_env.filters['sanitize_html'] = sanitize_html
app.jinja_env.filters['remove_blank'] = remove_blank
app.jinja_env.filters['gravatar_url'] = gravatar_url
app.jinja_env.filters['length'] = jinja_length

if not app.debug:
    print True
    # in production,logs must be recorded
    # from app.logs.log import DebugFalseLog
    #
    # handler = DebugFalseLog().get_handler()
    # app.logger.addHandler(handler)
    pass
