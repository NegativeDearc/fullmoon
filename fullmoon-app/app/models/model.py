# -*- coding:utf-8 -*-
from sqlalchemy import CheckConstraint
from .. import db


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
        status:
    }
    """
    __tablename__ = "Article"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True,nullable=False,unique=True)
    title = db.Column(db.String(25),nullable=True)
    content = db.Column(db.String(2000), nullable=True)
    tags = db.Column(db.String(25), nullable=True)
    create_date = db.Column(db.DATETIME, nullable=False)
    edit_date = db.Column(db.DATETIME, nullable=False)
    status = db.Column(db.String(10),nullable=False)

    # set constraint of status
    CheckConstraint('status IN ("PUBLISHED","DRAFTED","ARCHIVED","DELETED")',name='check_status')


# class Comment(db):
#     pass


class Login(db.Model):
    """
    table store user name and password
    """
    __tablename__ = 'Login'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True)
    user = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),unique=True,nullable=False)


# class Secure(db):
#     pass

if __name__ == "__main__":
    print db