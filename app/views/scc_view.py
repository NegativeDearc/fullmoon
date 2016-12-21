# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.models.model import Article

scc = Blueprint('scc',__name__,template_folder='templates',url_prefix='/scc')


@scc.route('/blog', methods=['GET','POST'])
def scc_root(page=1):
    pagination = Article.pagination(page=int(request.args.get('page',page)))
    latest_10 = Article.latest_article(page=int(request.args.get('page',page)))
    return render_template('SccBlog.html',latest_10=latest_10,pagination=pagination)


@scc.route('/blog/article/<string:uuid>')
def scc_administrator(uuid):
    article_by_uuid = Article.get_article_by_uuid(uuid=uuid)
    print article_by_uuid
    return render_template('ArticleTemplate.html',article_by_uuid = article_by_uuid)