# -*- coding:utf-8 -*-
from flask import Blueprint, render_template
from app.models.model import Article
from app import db

scc = Blueprint('scc',__name__,template_folder='templates',url_prefix='/scc')


@scc.route('/blog',methods=['GET','POST'])
def scc_root():
    latest_10 = Article.latest_article()
    print len(latest_10)
    for item in latest_10:
        print item
    return render_template('SccBlog.html',latest_10=latest_10)


@scc.route('/administrator')
def scc_administrator():
    return 'test'