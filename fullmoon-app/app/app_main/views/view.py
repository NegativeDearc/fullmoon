# -*- coding:utf-8 -*-

from flask import Blueprint

main = Blueprint('main',__name__,template_folder='templates')


@main.route('/')
@main.route('/index')
def main_root():
    return str('main page')