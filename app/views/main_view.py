# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.model import Article
from app import db

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
    return render_template('AboutTheWebsite.html')


@main.route('/editor', methods=['GET','POST'])
def main_edit():
    article_for_administration = Article.administration_article()
    print article_for_administration
    for x in article_for_administration:
        print x.__class__()
    if request.method == "POST":
        print request.form
        # 重复提交的问题：在页面多次保存之后会提交多份到数据库，实际需求是修改的动作
        # 考虑uuid的用法
        db.session.add(Article(request.form))
        db.session.commit()
        return redirect(url_for('main.main_edit'))
    return render_template('ArticleEditor.html',article_for_administration=article_for_administration)


@main.route('/administrator')
def main_administrator():
    return '1'