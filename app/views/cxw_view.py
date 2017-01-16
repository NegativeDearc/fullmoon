# -*- coding:utf-8 -*-
from flask import Blueprint, url_for, redirect, render_template, request, send_file, send_from_directory
from app.config import Config
from app.models.model import Article

cxw = Blueprint('cxw', __name__, url_prefix="/cxw")


@cxw.route('/blog')
@cxw.route('/blog/')
def cxw_blog():
    return render_template("CxwBlog.html")


@cxw.route('/about')
def cxw_about():
    pass


@cxw.route('/resume')
def cxw_resume():
    return render_template("ResumeShowcase.html")


@cxw.route('/resume/file/<string:filename>')
def cxw_resume_file(filename):
    return send_from_directory(Config.pdf_path, filename)
