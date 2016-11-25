# -*- coding:utf-8 -*-
from sqlalchemy import CheckConstraint, UniqueConstraint, desc
from app import db

# if you want use db.create_all()
# import all db models after import db from app


# noinspection PyPackageRequirements,PyPackageRequirements
class Article(db.Model):
    """
    A table store all articles for user.
    Include {
        id:
        title:
        content:
        tags:
        create_date:
        edit_date:
        read_times
        status:
    }
    """
    __tablename__ = "Article"
    # use table configuration to constraint columns or table
    __table_args__ = (
        # set constraint of status
        CheckConstraint('status IN ("PUBLISHED","DRAFTED","ARCHIVED","DELETED")',name='article_check_status'),
        UniqueConstraint('id','title')
    )
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True,nullable=False)
    title = db.Column(db.String(25),nullable=True)
    content = db.Column(db.String(2000), nullable=True)
    tags = db.Column(db.String(25), nullable=True)
    create_date = db.Column(db.DATETIME, nullable=False)
    edit_date = db.Column(db.DATETIME, nullable=False)
    # read_times = db.Column(db.INTEGER,default=1,nullable=False)
    status = db.Column(db.String(10),nullable=False)

    @staticmethod
    def latest_article():
        '''
        choose the lastest 10 artical information for showcase
        :return:
        '''
        return db.session.query(Article.title, Article.content, Article.tags, Article.create_date).\
            filter(Article.status=='PUBLISHED').\
            order_by(desc(Article.create_date)).\
            limit(10).\
            all()


# class Comment(db.Model):
#     pass


class Login(db.Model):
    """
    table store user name and password
    """
    __tablename__ = 'Login'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True)
    user = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),unique=True,nullable=False)


class Secure(db.Model):
    """
    table store visitor ip address and lock the unauthorised visitor
    """
    __tablename__ = "Secure"
    __table_args__ = (
        UniqueConstraint("id"),
        CheckConstraint('status IN ("LOCKED","UNLOCKED","BLACKLIST")',name='secure_check_status')
    )
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    ip_address = db.Column(db.String(15))
    blacklist = db.Column(db.BOOLEAN)
    visited_times_in_five_minutes = db.Column(db.INTEGER)
    unlock_time = db.Column(db.DATETIME)
    status = db.Column(db.String(10))


# class Visit(db.Model):
#     pass