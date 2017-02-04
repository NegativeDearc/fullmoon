# -*- coding:utf-8 -*-
from flask import request, g, make_response
from uuid import uuid1
from flask.ext.restful import Resource
from app.models.model import db, Article, Login, Comment
from sqlalchemy.exc import IntegrityError
from collections import OrderedDict
from sqlalchemy import asc
from app import auth


# no need to use jsonify to handling return values, restful-api will do it automatically for us
class ApiRoute(Resource):
    decorators = [auth.login_required]

    def get(self):
        token = g.user_.generate_auth_token()
        return {
            "token": token.decode("ascii"),
            "expires_in": 600
        }

    def post(self):
        token = g.user_.generate_auth_token()
        return {
            "token": token.decode("ascii"),
            "expires_in": 600
        }

    def put(self):
        pass

    def delete(self):
        pass


class ToolsApi(Resource):
    """
    generate uuid for "ArticleEditor".html
    """

    def get(self):
        return {'uuid': uuid1().__str__()}

    def post(self):
        return {'uuid': uuid1().__str__()}


class ArticleApi(Resource):
    """
    配合ajax方法进行restful设计，ajax的data加入{"_method":对应方式}
    程序会自动处理请求的方式，可以通过print request.form的方式进行验证
    """
    decorators = [auth.login_required]

    def get(self, uuid):
        rv = Article.article_by_uuid_api(uuid=uuid)
        return rv

    def post(self, uuid):
        """
        :param demands:不用需求场景的代码
        :param uuid: 识别文章的唯一代码
        :return:
        """
        uuid = request.form.get("uuid", '')
        demands = request.form.get("demands", '')

        if demands == "1":
            # make it JSON serializable
            rv = list(Article.status_ordered_list(uuid=uuid))
            return {"list": rv}, 200

    def put(self, uuid):
        """
        配合ArticleEditor.html页面的ajax PUT请求，进行更新动作。
        若没有uuid，则会进行插入动作，适合页面新增的需求
        若查询到uuid，可以进行部分字段的更新，
        :param uuid: 来自html页面不同需求场景下的值
        :return: {动作信息: http返回代码}
        """
        form = {k: None if v == '' else v for k, v in request.form.items()}
        # receive tags list, transfer list to string
        tags = request.form.getlist("tag[]")
        if tags:
            tags = ','.join(tags)
        else:
            tags = None

        form.update({"tags": tags})

        if Article.get_article_by_uuid(uuid=form.get('uuid'), abort=False):
            # article update logical here
            # check the form
            if Article.update_article(form):
                return {'message': 'update success'}, 200
            else:
                return {'message': 'update failed'}, 500
        else:
            try:
                # add new record
                db.session.add(Article(form))
                db.session.commit()
                return {'message': 'add success'}
            except IntegrityError:
                db.session.rollback()
                return {'message': 'add failed'}, 500

    def delete(self, uuid):
        """
        对指定uuid进行删除操作。
        :param uuid: 来自页面隐藏字段
        :return: json响应，包含多种信息
        """
        records = Article.query.filter(Article.uuid == uuid).first()
        if records:
            db.session.delete(records)
            db.session.commit()
            return {
                'uuid': uuid,
                'title': 'delete records from database by uuid',
                'description': records.__repr__() + ' has been deleted',
                'done': True
            }


class ApiComment(Resource):
    """
    apis for comments operation
    """

    decorators = [auth.login_required]

    def get(self, id):
        pass

    def post(self, id):
        pass

    def put(self, id):
        print request.form
        try:
            Comment.appr_message(row_id=request.form.get("_id_"))
            return {"message": "success"}, 200
        except Exception as e:
            print e
            return {"message": "failed"}, 500

    def delete(self, id):
        print request.form
        try:
            Comment.del_message(row_id=request.form.get("_id_"))
            return {"message": "success"}, 200
        except Exception as e:
            print e
            return {"message": "failed"}, 500
