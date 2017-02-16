# -*- coding:utf-8 -*-
from security import MailConfig
import os


class Config(object):
    CONFIG_NAME = 'config'
    DEBUG = None
    # flask-mail config
    MAIL_SERVER = 'smtpdm.aliyun.com'
    MAIL_PORT = 25
    MAIL_USERNAME = MailConfig.MAIL_USERNAME
    MAIL_PASSWORD = MailConfig.MAIL_PASSWORD
    MAIL_DEFAULT_SENDER = MailConfig.MAIL_DEFAULT_SENDER
    MAIL_DEBUG = True
    # register static fold path for all blueprint
    static_path = os.path.join(os.path.dirname(__file__), 'static')
    pdf_path = os.path.join(os.path.dirname(__file__), 'static', 'pdf')
    # celery config
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    CELERY_TIMEZONE = "Asia/Shanghai"
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    CELERYD_POOL_RESTARTS = True
    CELERYD_TASK_TIME_LIMIT = 60 * 10

    # register template fold path for all blueprint
    @classmethod
    def template_path(cls, postfix=None):
        return os.path.join(os.path.dirname(__file__), 'templates', str(postfix))

    @staticmethod
    def upload_path():
        return os.path.join(os.path.dirname(__file__), 'static', 'upload')

    # security keys of flask
    SECRET_KEY = '26e9e25a-b0b5-11e6-9db0-60f81dba2c0c'
    # sqlalchemry settings
    # For Unix: sqlite:/// /absolute/path/to/database
    # For Win: sqlite:/// c:/absolute/path/to/database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.abspath(
                                  os.path.join(os.path.dirname(__file__), 'models', 'test.db')
                              )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

    PIC_ALLOW_POSTFIX = {".jpeg", '.jpg', '.png', '.bmp'}  # == set([])
    PIC_ALLOW_POSTFIX_WITHOUT_DOT = {"jpeg", 'jpg', 'png', 'bmp'}  # == set([])


class ProductionConfig(Config):
    CONFIG_NAME = 'production'
    MAIL_DEBUG = False
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    CONFIG_NAME = 'development'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # only for test database initialization
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'default': Config,
    'production': ProductionConfig,
    'development': DevelopmentConfig
}
