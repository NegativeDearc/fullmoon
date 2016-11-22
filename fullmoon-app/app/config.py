# -*- coding:utf-8 -*-
import os


class Config(object):
    # 蓝图注册static文件夹地址
    static_path = os.path.join(os.path.dirname(__file__),'static')
    SECRET_KEY = '26e9e25a-b0b5-11e6-9db0-60f81dba2c0c'
    SQLALCHEMY_DATABASE_URI = os.path.join(os.path.dirname(__file__),'models/')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


config = {
    'production': ProductionConfig,
    'Development': DevelopmentConfig
}