# -*- coding:utf-8 -*-
from flask import Blueprint, request
from uuid import uuid1
from flask.ext.restful import Resource
from app.models.model import db, Article, Visit
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc


# no need to use jsonify to handling return values, restful-api will do it automatically for us
class ToolsApi(Resource):
    '''
    generate uuid for "ArticleEditor".html
    '''

    def get(self):
        return {'uuid': uuid1().__str__()}

    def post(self):
        return {'uuid': uuid1().__str__()}


class ArticleApi(Resource):
    '''
    配合ajax方法进行restful设计，ajax的data加入{"_method":对应方式}
    程序会自动处理请求的方式，可以通过print request.form的方式进行验证
    '''

    def get(self, uuid):
        rv = Article.article_by_uuid_api(uuid=uuid)
        return rv

    def post(self, uuid):
        pass

    def put(self, uuid):
        print uuid
        form = {k: None if v == '' else v for k, v in request.form.items()}

        if Article.get_article_by_uuid(uuid=form.get('uuid'), abort=False):
            print Article.get_article_by_uuid(uuid=form.get('uuid'), abort=False)
            # article update logical here
            # check the form
            if Article.update_article(form):
                return {'message': 'update'}, 200
            else:
                return {'message': 'failed'}, 500
        else:
            try:
                # add new record
                db.session.add(Article(form))
                db.session.commit()
                return {'message': 'add'}
            except IntegrityError:
                db.session.rollback()
                return {'message': 'failed'}, 500

    def delete(self, uuid):
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
        Visit.query.update({'times':origin_visit_times+1})
        db.session.commit()
        return {
            "times":origin_visit_times
        }