# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.model import Article
from flask.ext.login import login_required

scc = Blueprint('scc', __name__, template_folder='templates', url_prefix='/scc')


@scc.route('/blog', methods=['GET', 'POST'])
def scc_root(page=1):
    if request.args.get("article", ""):
        return redirect(url_for("scc.scc_article", uuid=request.args.get("article")))
    pagination = Article.pagination(page=int(request.args.get('page', page)), author='scc')
    latest_10 = Article.latest_article(page=int(request.args.get('page', page)), author='scc')
    return render_template('SccBlog.html', latest_10=latest_10, pagination=pagination)


@scc.route('/blog/article/<string:uuid>', methods=['GET', 'POST'])
def scc_article(uuid):
    if request.args.get('edit') == 'true':
        return redirect(url_for("scc.article_editor", uuid=uuid))
    article_by_uuid = Article.get_article_by_uuid(uuid=uuid)
    return render_template('ArticleTemplate.html', article_by_uuid=article_by_uuid)


@scc.route('/blog/article/<string:uuid>/editor')
@login_required
def article_editor(uuid):
    article_by_uuid = Article.get_article_by_uuid(uuid=uuid)
    return render_template('ArticleTemplate.html', article_by_uuid=article_by_uuid, scripts=True)
