# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def main_root():
    return render_template('WelcomePage.html')


@main.route('/login',methods=['GET','POST'])
def main_login():
    return render_template('YouMustLogin.html')


@main.route('/about')
def main_about():
    return render_template('About the Website.html')


@main.route('/editor')
def main_edit():
    return render_template('ArticleEditor.html')


@main.route('/administrator')
def main_administrator():
    return '1'