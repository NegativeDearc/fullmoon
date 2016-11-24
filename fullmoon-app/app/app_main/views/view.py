# -*- coding:utf-8 -*-

from flask import Blueprint, render_template

main = Blueprint('main',__name__)


@main.route('/')
@main.route('/index')
def main_root():
    print main.root_path
    print main.static_folder
    print main.template_folder
    return render_template('WelcomePage.html')


@main.route('/login',methods=['GET','POST'])
def main_login():
    return render_template('YouMustLogin.html')


@main.route('/about')
def main_about():
    return render_template('About the Website.html')


@main.route('/administrator')
def main_administrator():
    return '1'