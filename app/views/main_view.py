# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response, g, flash, session
from app.models.model import Article, Visit, Login
from flask.ext.login import login_required, login_user, current_user, logout_user

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def main_root():
    return render_template('WelcomePage.html')


@main.route('/login', methods=['GET', 'POST'])
def main_login():
    if current_user.is_authenticated:
        return redirect(url_for("main.main_edit"))
    if request.method == "POST":
        user = Login.query.filter(Login.user == request.form.get("usr")).first()
        if user is not None and user.verify_password(request.form.get("pwd")):
            login_user(user, remember=True)
            return redirect(request.args.get("next")) or url_for("main.main_root")
        else:
            flash('Wrong user name or password')
    return render_template('YouMustLogin.html')


@main.route('/about')
def main_about():
    return render_template('AboutTheWebsite.html')


@main.route('/editor', methods=['GET', 'POST'])
@login_required
def main_edit():
    print session
    article_for_administration = Article.administration_article(user=current_user.user)
    return render_template('ArticleEditor.html', article_for_administration=article_for_administration)


@main.route('/administrator')
@login_required
def main_administrator():
    return '1'
