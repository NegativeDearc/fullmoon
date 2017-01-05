# -*- coding:utf-8 -*-
from flask import Blueprint, request, g, make_response
from uuid import uuid1
from flask.ext.restful import Resource
from app.models.model import db, Article, Visit, Login
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
        pass

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
        print form

        if Article.get_article_by_uuid(uuid=form.get('uuid'), abort=False):
            # article update logical here
            # check the form
            if Article.update_article(form):
                print "trying to update"
                return {'message': 'update success'}, 200
            else:
                return {'message': 'update failed'}, 500
        else:
            try:
                # add new record
                print "trying to add"
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


class VisitTimes(Resource):
    # 记录页面访问次数的API，应该覆盖全部页面
    # 每访问一次增加一条记录
    def put(self):
        origin_visit_times = Visit().visit_times
        Visit.query.update({'times': origin_visit_times + 1})
        db.session.commit()
        return {
            "times": origin_visit_times
        }
