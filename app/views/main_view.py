# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response, g, flash
from app.models.model import Article, Visit
from flask.ext.login import login_required, login_user, current_user

main = Blueprint('main', __name__)


@main.before_request
def before_request():
    g.user = current_user


@main.route('/')
@main.route('/index')
def main_root():
    return render_template('WelcomePage.html')


@main.route('/login', methods=['GET', 'POST'])
def main_login():
    if request.method == "POST":
        # verify the login user if authenticated
        help(login_user)
        if not g.user.is_authenticated:
            flash('Wrong user name or password')

        if g.user is not None and g.user.is_authenticated:

            print 'user is authenticated'
            return request.args.get("next")
    return render_template('YouMustLogin.html')


@main.route('/about')
def main_about():
    return render_template('AboutTheWebsite.html')


@main.route('/editor', methods=['GET','POST'])
@login_required
def main_edit():
    article_for_administration = Article.administration_article()
    return render_template('ArticleEditor.html',article_for_administration=article_for_administration)


@main.route('/administrator')
@login_required
def main_administrator():
    return '1'