from flask import Blueprint, url_for, render_template

scc = Blueprint('scc',__name__,template_folder='templates',url_prefix='/scc')


@scc.route('/blog')
def scc_root():
    return render_template('SccBlog.html')


@scc.route('/administrator')
def scc_administrator():
    return 'test'