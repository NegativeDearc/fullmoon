# -*- coding:utf-8 -*-
from sqlalchemy import CheckConstraint, UniqueConstraint, desc
from sqlalchemy.orm.exc import NoResultFound
from database import db
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin


# if you want use db.create_all()
# import all db models after import db from app
class Article(db.Model):
    """
    A table store all articles for user.
    Include {
        id: autoincrement primary key
        uuid:unique id for article,generate by time
        title:title of article
        content:content of article
        tags:tags generate by machine learning
        create_date:the created time of article,can't be edit or update,how?
        edit_date:date time when the article edited
        read_times:record read times when the article was read. use js?
        status:status of article "PUBLISHED","DRAFTED","ARCHIVED","DELETED"
    }
    """
    __tablename__ = "Article"
    # use table configuration to constraint columns or table
    # not null != ''
    __table_args__ = (
        # set constraint of status
        CheckConstraint('status IN ("PUBLISHED","DRAFTED","ARCHIVED","DELETED")', name='article_check_status'),
        UniqueConstraint('id', 'title')
    )
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, unique=True)
    uuid = db.Column(db.String(20), nullable=False, unique=True)
    author = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    tags = db.Column(db.String(25), nullable=True)
    create_date = db.Column(db.DATETIME, nullable=False)
    edit_date = db.Column(db.DATETIME, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    read_times = db.Column(db.INTEGER, default=1, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __init__(self, form={}):
        self.uuid = form.get('uuid', None)
        self.title = form.get('title', None)
        self.author = form.get('author', None)
        self.content = form.get('content', None)
        self.tags = None
        self.create_date = datetime.now()
        self.edit_date = datetime.now()
        self.category = ''
        self.read_times = ''
        self.status = form.get('status', None)

    def __repr__(self):
        return "at %s created an article named %s and it's content %s" % \
               (self.create_date, self.title, self.content)

    @classmethod
    def update_article(cls, form={}):
        # update by request form, be careful with the date time handling
        # "2016-12-22T03:30:24.160Z"
        # %a 星期的简写。如 星期三为Web
        # %A 星期的全写。如 星期三为Wednesday
        # %b 月份的简写。如4月份为Apr
        # %B 月份的全写。如4月份为April
        # %c:  日期时间的字符串表示。（如： 04/07/10 10:43:39）
        # %d:  日在这个月中的天数（是这个月的第几天）
        # %f:  微秒（范围[0,999999]）
        # %H:  小时（24小时制，[0, 23]）
        # %I:  小时（12小时制，[0, 11]）
        # %j:  日在年中的天数 [001,366]（是当年的第几天）
        # %m:  月份（[01,12]）
        # %M:  分钟（[00,59]）
        # %p:  AM或者PM
        # %S:  秒（范围为[00,61]，为什么不是[00, 59]）
        # %U:  周在当年的周数当年的第几周），星期天作为周的第一天
        # %w:  今天在这周的天数，范围为[0, 6]，6表示星期天
        # %W:  周在当年的周数（是当年的第几周），星期一作为周的第一天
        # %x:  日期字符串（如：04/07/10）
        # %X:  时间字符串（如：10:43:39）
        # %y:  2个数字表示的年份
        # %Y:  4个数字表示的年份
        # %z:  与utc时间的间隔 （如果是本地时间，返回空字符串）
        # %Z:  时区名称（如果是本地时间，返回空字符串）
        cls.query.filter(cls.uuid == form.get('uuid')).update({
            'title': form.get('title'),
            'content': form.get('content'),
            # UTC 时间，需要加上8小时才是中国时间GMT+8
            'edit_date': datetime.strptime(form.get('edit_date'), '%Y-%m-%dT%H:%M:%S.%fZ'),
            'status': form.get('status')
        })
        db.session.commit()
        return True

    @classmethod
    def get_article_by_uuid(cls, uuid, abort=True):
        # get article by query of uuid
        # write uuid judgement here,use re module as a practise
        # 0e3a6e0f-c720-11e6-852c-f4066974556c
        if abort:
            return cls.query.filter(cls.uuid == uuid, cls.status == 'PUBLISHED').first_or_404()
        else:
            try:
                cls.query.filter(cls.uuid == uuid).one()
                return True
            except NoResultFound:
                return False

    @classmethod
    def latest_article(cls, page=1):
        # get articles which are in published status
        n = page * 5
        return cls.query. \
                   filter(cls.status == 'PUBLISHED'). \
                   order_by(desc(cls.create_date)). \
                   all()[n - 5:n]

    @classmethod
    def pagination(cls, page):
        # get paginate of query
        return cls.query.paginate(page, per_page=5, error_out=True)

    @classmethod
    def administration_article(cls, user=None, category="all"):
        # get the article by category
        return cls.query.filter(cls.author == user).all()

    @classmethod
    def article_by_uuid_api(cls, uuid):
        try:
            rv = cls.query.filter(cls.uuid == uuid).one()
            return {
                'uuid': uuid,
                'title': 'query article by uuid',
                'description': rv.__repr__(),
                'done': True
            }
        except NoResultFound:
            return {
                'uuid': uuid,
                'title': 'query article by uuid',
                'description': 'query article by uuid, not limited by status of article',
                'done': False
            }


# class Comment(db.Model):
#     pass


class Login(db.Model, UserMixin):
    """
    table store user name and password
    Include {
        id:autoincrement primary key
        user:user name encrypted by salt,can't be read
        password:encrypted by salt,can't be read
    }
    """
    __tablename__ = 'Login'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, unique=True)
    user = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=True)

    def __init__(self, user=None, password=None, mail=None):
        self.user = user
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha1", salt_length=16)
        self.mail = mail

    @property
    def password(self):
        raise AttributeError("You Can't Read the Original Password!")

    # user.password='password'
    @password.setter
    def password(self, password=None):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha1", salt_length=16)

    def verify_password(self, password=None):
        if password is None:
            return False
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return False

    def get_id(self):
        """
        get user id from profile file, if not exist, it will
        generate a uuid for the user.
        :return:unicode
        """
        if self.user is not None:
            return unicode(self.id)
        return unicode(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """
        try to return user_id corresponding User object.
        This method is used by load_user callback function
        :param user_id:
        :return:Login class
        """
        if not user_id:
            return None
        else:
            login = Login.query.filter(Login.id == user_id).one()
            return login


class Secure(db.Model):
    """
    table store visitor ip address and lock the unauthorised visitor
    """
    __tablename__ = "Secure"
    __table_args__ = (
        UniqueConstraint("id"),
        CheckConstraint('status IN ("LOCKED","UNLOCKED","BLACKLIST")', name='secure_check_status')
    )
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
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
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    times = db.Column(db.INTEGER)
    update_time = db.Column(db.DATETIME)

    @property
    def visit_times(self):
        return db.session.query(Visit.times).first()[0]


if __name__ == '__main__':
    db.create_all()