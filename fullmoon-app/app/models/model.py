# -*- coding:utf-8 -*-
from sqlalchemy import CheckConstraint, UniqueConstraint
from .. import db

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
        status:
    }
    """
    __tablename__ = "Article"
    # use table configuration to constraint columns or table
    __table_args__ = (
        # set constraint of status
        CheckConstraint('status IN ("PUBLISHED","DRAFTED","ARCHIVED","DELETED")',name='check_status'),
        UniqueConstraint('id','title')
    )
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True,nullable=False)
    title = db.Column(db.String(25),nullable=True)
    content = db.Column(db.String(2000), nullable=True)
    tags = db.Column(db.String(25), nullable=True)
    create_date = db.Column(db.DATETIME, nullable=False)
    edit_date = db.Column(db.DATETIME, nullable=False)
    status = db.Column(db.String(10),nullable=False)


class Comment(db):
    pass


class Login(db.Model):
    """
    table store user name and password
    """
    __tablename__ = 'Login'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True)
    user = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),unique=True,nullable=False)


class Secure(db):
    """
    table store visitor ip address and lock the unauthorised visitor
    """
    __tablename__ = "Secure"
    __table_args__ = (
        UniqueConstraint("id"),
        CheckConstraint('status IN ("LOCKED","UNLOCKED","BLACKLIST")')
    )
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    ip_address = db.Column(db.String(15))
    blacklist = db.Column(db.BOOLEAN)
    visited_times_in_five_minutes = db.Column(db.INTEGER)
    unlock_time = db.Column(db.DATETIME)
    status = db.Column(db.String(10))

if __name__ == "__main__":
    print db