# -*- coding:utf-8 -*-
from flask import Blueprint, url_for, redirect, render_template, request, send_file, send_from_directory
from app.config import Config
from app.models.model import Article
from flask.ext.login import login_required

cxw = Blueprint('cxw', __name__, url_prefix="/cxw")


@cxw.route('/blog')
@cxw.route('/blog/')
def cxw_blog():
    if request.args.get("article", ""):
        return url_for("cxw.cxw_article", uuid=request.args.get("article"))

    published_article = Article.get_published_article(usr='cxw')
    return render_template("CxwBlog.html", published_article=published_article)


@cxw.route("/blog/article/<string:uuid>", methods=["GET", "POST"])
def cxw_article(uuid):
    article = Article.get_article_by_uuid(uuid=uuid)

    if request.args.get("edit") == "true":
        return redirect(url_for("cxw.cxw_article_editor", uuid=uuid))
    if request.method == "POST":
        pass

    return render_template("ArticleTemplateTheme_1.html", article=article)


@cxw.route("/blog/article/<string:uuid>/editor", methods=["GET", "POST"])
@login_required
def cxw_article_editor(uuid):
    article = Article.get_article_by_uuid(uuid=uuid)

    if request.method == "POST":
        print request.form
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
