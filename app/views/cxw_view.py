# -*- coding:utf-8 -*-
from flask import Blueprint, url_for, redirect, render_template, request, send_file, send_from_directory
from datetime import datetime
from app.config import Config
from app.models.model import Article, Comment
from flask.ext.login import login_required, logout_user
from app import db

cxw = Blueprint('cxw', __name__, url_prefix="/cxw")


@cxw.route('/blog')
@cxw.route('/blog/')
def cxw_blog():
    if request.args.get("article", ""):
        return redirect(url_for("cxw.cxw_article", uuid=request.args.get("article")))

    archive = Article.archive_statistic(author="cxw")
    published_article = Article.get_published_article(usr='cxw')
    return render_template("CxwBlog.html", published_article=published_article, archive=archive)


@cxw.route("/blog/article/<string:uuid>", methods=["GET", "POST"])
def cxw_article(uuid):
    article = Article.get_article_by_uuid(uuid=uuid)

    if request.args.get("edit") == "true":
        return redirect(url_for("cxw.cxw_article_editor", uuid=uuid))
    if request.args.get("logout") == "true":
        logout_user()
        return redirect(url_for("cxw.cxw_article", uuid=uuid))

    if request.method == "POST":
        db.session.add(Comment(
            uid=uuid,
            rdr_name=request.form.get("nickname"),
            rdr_mail=request.form.get("mail-address"),
            rdr_message=request.form.get("comment-content"),
            reply_to_id=request.form.get("reply_to_id")
        ))
        db.session.commit()
        return redirect(url_for("cxw.cxw_article", uuid=uuid))
    return render_template("ArticleTemplateTheme_1.html", article=article)


@cxw.route("/blog/article/<string:uuid>/editor", methods=["GET", "POST"])
@login_required
def cxw_article_editor(uuid):
    article = Article.get_article_by_uuid(uuid=uuid)

    if request.method == "POST":
        db.session.query(Article).filter(Article.uuid == uuid).update({
            "title": request.form.get("title"),
            "content": request.form.get("ckeditor"),
            "edit_date": datetime.now()
        })
        db.session.commit()
        return redirect(url_for("cxw.cxw_article", uuid=uuid))
    return render_template("ArticleTemplateTheme_1.html", article=article, edit=True)


@cxw.route('/about')
def cxw_about():
    pass


@cxw.route('/resume')
@cxw.route('/resume/')
def cxw_resume():
    return render_template("ResumeShowcase.html")


@cxw.route('/resume/file/<string:filename>')
def cxw_resume_file(filename):
    return send_from_directory(Config.pdf_path, filename)
