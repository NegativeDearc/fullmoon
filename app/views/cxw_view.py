# -*- coding:utf-8 -*-
from flask import Blueprint, url_for, redirect


cxw = Blueprint('cxw', __name__, url_prefix="/dearc")


@cxw.route('/about')
def cxw_about():
    pass

