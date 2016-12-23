# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from app.models.model import Article, Visit

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
    return render_template('ArticleEditor.html',article_for_administration=article_for_administration)


@main.route('/administrator')
def main_administrator():
    return '1'