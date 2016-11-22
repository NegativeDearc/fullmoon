from flask import Blueprint, url_for

scc = Blueprint('scc',__name__,template_folder='templates',url_prefix='/scc')


@scc.route('/')
def root():
    return str(scc.static_folder)