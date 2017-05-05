# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.model import db, Article, Comment
from flask.ext.login import login_required, logout_user
from datetime import datetime

scc = Blueprint('scc', __name__, template_folder='templates', url_prefix='/scc')


@scc.route('/blog', methods=['GET', 'POST'])
def scc_root(page=1):
    recent_articles = Article.recent_articles(author='scc')
    recent_comments = Comment.recent_comments(author='scc')
    archive = Article.archive_statistic(author="scc")

    if request.args.get("article", ""):
        # redirect to article URL if get the ?article=uuid
        return redirect(url_for("scc.scc_article", uuid=request.args.get("article")))

    pagination = Article.pagination(page=int(request.args.get('page', page)), author='scc')
    latest_10 = Article.latest_article(page=int(request.args.get('page', page)), author='scc')
    return render_template('SccBlog.html',
                           latest_10=latest_10,
                           pagination=pagination,
                           recent_articles=recent_articles,
                           recent_comments=recent_comments,
                           archive=archive)


@scc.route('/blog/article/<string:uuid>', methods=['GET', 'POST'])
def scc_article(uuid):
    if request.args.get('edit') == 'true':
        return redirect(url_for("scc.article_editor", uuid=uuid))
    if request.args.get("logout") == "true":
        logout_user()

    if request.method == "POST":
        db.session.add(Comment(
            uid=uuid,
            rdr_name=request.form.get("nickname"),
            rdr_mail=request.form.get("mail-address"),
            rdr_message=request.form.get("comment-content"),
            reply_to_id=request.form.get("reply_to_id")
        ))
        db.session.commit()
        return redirect(url_for("scc.scc_article", uuid=uuid))
    article_by_uuid = Article.get_article_by_uuid(uuid=uuid)
    return render_template('ArticleTemplate.html', article_by_uuid=article_by_uuid)


@scc.route('/blog/article/<string:uuid>/editor', methods=['GET', 'POST'])
@login_required
def article_editor(uuid):
    if request.args.get("logout") == "true":
        logout_user()
        return redirect(url_for("scc.scc_article", uuid=uuid))

    article_by_uuid = Article.get_article_by_uuid(uuid=uuid, abort=False)
    if request.method == 'POST':
        # update article then redirect to the article url
        # if need to re-edit, just push the back to history button at browser
        db.session.query(Article).filter(Article.uuid == uuid).update({
            "title": request.form.get("title"),
            "content": request.form.get("content"),
            "edit_date": datetime.now()
        })
        db.session.commit()
        return redirect(url_for("scc.scc_article", uuid=uuid))
    return render_template('ArticleTemplate.html', article_by_uuid=article_by_uuid, scripts=True)


@scc.route('/blog/archive/<string:date_filter>')
def archive_all(date_filter):
    archive = Article.archive(date_filter=date_filter, author="scc")
    return render_template("AllArticle.html", archive=archive)