# -*- coding:utf-8 -*-
import os


class Config(object):
    # register static fold path for all blueprint
    static_path = os.path.join(os.path.dirname(__file__), 'static')

    # register template fold path for all blueprint
    @classmethod
    def template_path(self, postfix=None):
        return os.path.join(os.path.dirname(__file__), 'templates', str(postfix))

    # security keys of flask
    SECRET_KEY = '26e9e25a-b0b5-11e6-9db0-60f81dba2c0c'
    # sqlalchemry settings
    # For Unix: sqlite:////absolute/path/to/database
    # For Win: sqlite:///c:/absolute/path/to/database
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + \
                              os.path.abspath(
                                  os.path.join(os.path.dirname(__file__),'models','test.db')
                              )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # only for test database initialization
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'production': ProductionConfig,
    'Development': DevelopmentConfig
}
