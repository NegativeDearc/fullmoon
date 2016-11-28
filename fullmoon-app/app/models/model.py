# -*- coding:utf-8 -*-
from sqlalchemy import CheckConstraint, UniqueConstraint, desc
from app import db

# if you want use db.create_all()
# import all db models after import db from app


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

    @classmethod
    def latest_article(cls, page=1):
        n = page * 5
        return cls.query.\
            filter(cls.status=='PUBLISHED').\
            order_by(desc(cls.create_date)).\
            all()[n-5:n]

    @classmethod
    def pagination(cls, page):
        return cls.query.paginate(page,per_page=5,error_out=True)

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

    def is_authenticated(self):
        pass

    def is_active(self):
        pass

    def is_anonymous(self):
        pass

    def get_id(self):
        pass

    def verify_password(self):
        pass


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


class Visit(db.Model):
    """
    table store website visit times
    """
    __tablename__ = "Visit"
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    times = db.Column(db.INTEGER)
    update_time = db.Column(db.DATETIME)