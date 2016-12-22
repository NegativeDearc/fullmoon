# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from app.models.model import Article
from app import db
from sqlalchemy.exc import IntegrityError

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

    if request.method == "POST":
        # not null != '' , prevent '' insert to database
        form = {k:None if v == '' else v for k,v in request.form.items()}
        print form
        # query Article by uuid ,if existed,update it. else add a new record
        if Article.get_article_by_uuid(uuid=form.get('uuid'),abort=False):
            print Article.get_article_by_uuid(uuid=form.get('uuid'),abort=False)
            # article update logical here
            # check the form
            if Article.update_article(form):
                return jsonify({'message':'update'}), 200
            else:
                return jsonify({'message':'failed'}), 500
        else:
            try:
                # add new record
                db.session.add(Article(form))
                db.session.commit()
                return jsonify({'message': 'add'})
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': 'failed'}), 500
    return render_template('ArticleEditor.html',article_for_administration=article_for_administration)


@main.route('/administrator')
def main_administrator():
    return '1'