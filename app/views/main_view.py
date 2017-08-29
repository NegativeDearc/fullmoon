# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response, g, flash, session, \
    abort, current_app
from sqlalchemy.orm.exc import NoResultFound
from app.models.model import Article, Login, Comment
from flask.ext.login import login_required, login_user, current_user, logout_user, login_fresh, login_url
from app.config import ProductionConfig

import os
import time
from datetime import datetime, timedelta
from json import dumps


main = Blueprint('main', __name__)


@main.before_request
def before_request():
    g.user = current_user


@main.route('/')
@main.route('/index')
def main_root():
    return render_template('WelcomePage.html')


@main.route('/sitemap.xml')
def main_sitemap():
    pages = []
    users = Article.query.order_by(Article.author).filter(Article.status == "PUBLISHED").all()

    for user in users:
        if user.author == "cxw":
            url = url_for('cxw.cxw_article', uuid=user.uuid)[1:]
        elif user.author == "scc":
            url = url_for('scc.scc_article', uuid=user.uuid)[1:]

        modified_time = user.edit_date.date().isoformat()
        pages.append([url, modified_time])

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@main.route('/robots.txt')
def main_robots():
    robots_text = render_template('robots.txt')
    response = make_response(robots_text)
    response.headers["Content-Type"] = "text/plain"
    return response


@main.route('/login', methods=['GET', 'POST'])
def main_login():
    if current_user.is_authenticated:
        return redirect(url_for("main.main_edit"))
    if request.method == "POST":
        user = Login.query.filter(Login.user == request.form.get("usr")).first()
        if user is not None and user.verify_password(request.form.get("pwd")):
            login_user(user, remember=True, force=True, fresh=True)  # it will return True if success
            if not request.args.get("next"):  # if get None , redirect to main.main_edit
                return redirect(url_for("main.main_edit"))
            return redirect(request.args.get("next"))
        else:
            flash('Wrong user name or password')
    return render_template('YouMustLogin.html')


@main.route("/reset", methods=["GET", "POST"])
def main_reset_password():
    session.mail_send_for_reset = None

    if request.method == "POST":
        mail = request.form.get("user")
        try:
            Login.query.filter(Login.mail == mail).one()
            session.mail_send_for_reset = mail
            # print(session.mail_send_for_reset)
            # send verify mail background by celery
            Login.generate_reset_url(mail=mail)
            return jsonify({"message": "mail verify ok"}), 200
        except NoResultFound:
            return jsonify({"message": "No Result Found"}), 500
    return render_template("ForgetPassword.html")


@main.route("/reset-action/<string:token>", methods=["GET", "POST"])
def main_reset_action(token):
    mail = Login.verify_reset_token(token)
    if mail is None:
        abort(401)

    if request.method == "POST":
        if request.form.get("pwd1") == request.form.get("pwd2") and \
                        request.form.get("captcha") == session.get("captcha"):
            Login.update_password(mail, request.form.get("pwd1"))
            return jsonify({"message": "password changed"}), 200
        else:
            return jsonify({"message": "data not validated"}), 500
    return render_template("ResetPassword.html")


@main.route('/pdfRender')
def main_pdf_render():
    url = ''
    if request.args.get('file'):
        url = request.args.get('file')
    return render_template("PDFviewer.html", url=url)


@main.route('/editor', methods=['GET', 'POST'])
@login_required
def main_edit():
    article_for_administration = Article.administration_article(user=current_user.user)
    if request.args.get("logout") == "True":
        # Logs a user out. (You do not need to pass the actual user.)
        # This will also clean up the remember me
        # bug:AttributeError: 'AnonymousUserMixin' object has no attribute 'user'
        # By default, when a user is not actually logged in,
        # current_user is set to an AnonymousUserMixin object.
        logout_user()
        return redirect(url_for("main.main_login"))
    return render_template('ArticleEditor.html', article_for_administration=article_for_administration)


@main.route('/editor/upload_image', methods=["POST"])
@login_required
def main_upload_img():
    # http://www.tuicool.com/articles/AziEfq
    error = ''
    if request.method == 'POST' and "upload" in request.files:
        # ckeditor generate csrf token, named as "ckCsrfToken", how to use it?
        callback = request.args.get('CKEditorFuncNum')
        f = request.files['upload']
        # todo: use standard library to detect the postfix of picture
        # https://docs.python.org/2/library/imghdr.html
        postfix = '.'+(f.content_type.split("/")[-1])
        filename = time.strftime("%Y%m%d%H%M%S", time.localtime()) + postfix
        # to check the file extension
        if postfix in ProductionConfig.PIC_ALLOW_POSTFIX:
            if os.path.exists(os.path.join(main.static_folder, "upload")):
                save_path = os.path.join(main.static_folder, "upload", filename)
                f.save(save_path)
            else:
                os.mkdir(os.path.join(main.static_folder, "upload"))
                error = 'making directory...please refresh'
        else:
            error = 'file extension is not allowed!'

        f_url = '/'.join([main.static_url_path, "upload", filename])

        response = make_response("""
            <script>window.parent.CKEDITOR.tools.callFunction(%s,'%s','%s');</script>
        """ % (callback, f_url, error))
        response.headers["Content-Type"] = "text/html"
        return response


@main.route('/verify_token', methods=["GET", "POST"])
@login_required
def main_get_token():
    token = request.form.get("token")
    user = g.user.verify_auth_token(token)
    if user:
        return "test"
    else:
        abort(401)


@main.route('/get_token', methods=["GET", "POST"])
@login_required
def main_verify_token(expires=600):
    token = g.user.generate_auth_token(expiration=expires)
    return jsonify({"token": token})


@main.route('/render_temp/temp_1')
@login_required
def main_temp_1():
    # render article information by user
    article_for_administration = Article.administration_article(user=current_user.user)
    return render_template("article_info_temp.html", article_for_administration=article_for_administration)


@main.route('/render_temp/temp_2')
def main_temp_2():
    uuid = request.args.get("uuid")
    # render comments by uuid
    # we don't need to login to see comments
    # how to get comments data? By api or by url?
    comments = Comment.show_message(uuid=uuid)
    return render_template("comment_info_temp.html", comments=comments)


@main.route('/render_temp/temp_3')
@login_required
def main_temp_3():
    comments = Comment.approved_message()
    return render_template("comments_info_temp.html", comments=comments)


@main.route('/render_temp/temp_4')
@login_required
def main_temp_4():
    # render template for static file management
    rv = []
    path = ProductionConfig.upload_path()
    for pic in os.listdir(path):
        if pic.split('.')[-1] in ProductionConfig.PIC_ALLOW_POSTFIX_WITHOUT_DOT:
            temp = Article.search_pic_use(t=pic)
            url = '/'.join([main.static_url_path, "upload", pic])
            if temp:
                rv.append({"No": pic, "url": url, "content": temp})
            else:
                rv.append({"No": pic, "url": url, "content": None})
    return render_template("uploaded_files_management_temp.html", rv=rv)


@main.route('/render_temp/temp_5')
@login_required
def main_temp_5():
    dash = Article.dashboard(author=current_user.user)
    return render_template("dash_info_temp.html", dash_d=dumps(dash), dash=dash)