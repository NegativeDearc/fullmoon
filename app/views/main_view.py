# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response, g, flash, session, \
    abort
from app.models.model import Article, Login, Comment
from flask.ext.login import login_required, login_user, current_user, logout_user, login_fresh, login_url
from app.config import ProductionConfig
import os
import time

main = Blueprint('main', __name__)


@main.before_request
def before_request():
    g.user = current_user


@main.route('/')
@main.route('/index')
def main_root():
    return render_template('WelcomePage.html')


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
    print rv
    return render_template("uploaded_files_management_temp.html", rv=rv)
