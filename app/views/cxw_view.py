# -*- coding:utf-8 -*-
from flask import Blueprint, url_for, redirect, render_template


cxw = Blueprint('cxw', __name__, url_prefix="/cxw")


@cxw.route('/about')
def cxw_about():
    pass


@cxw.route('/resume')
def cxw_resume():
    return render_template("ResumeShowcase.html")