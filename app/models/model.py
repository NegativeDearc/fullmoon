# -*- coding:utf-8 -*-
from sqlalchemy import CheckConstraint, UniqueConstraint, desc, asc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.sql.expression import text, HasCTE
from database import db
import uuid
from datetime import datetime
from collections import OrderedDict
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from flask.ext.login import UserMixin
from app.config import config


# global method
def gen_uid():
    return uuid.uuid1().__str__()


def gen_dat():
    return datetime.now()


# extension for Comment
class ExtensionForComment(MapperExtension):
    pass


# extension for Visit DB
class ExtensionForVisit(MapperExtension):
    def before_update(self, mapper, connection, instance):
        print "instance %s before insert !" % instance


# extension for Article
class ExtensionForArticle(MapperExtension):
    pass


# extension for Login
class ExtensionForLogin(MapperExtension):
    pass


# extension for Security
class ExtensionForSecurity(MapperExtension):
    pass


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
    uuid = db.Column(db.String(50), nullable=False, unique=True)
    author = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
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
        # add encode to utf-8 otherwise it will get an error can't decode to ascii
        return "at %s created an article named %s and it's content %s" % \
               (self.create_date, self.title.encode("utf-8"), self.content.encode("utf-8"))

    @classmethod
    def update_article(cls, form={}):
        """
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
        :param form:
        :return:
        """
        cls.query.filter(cls.uuid == form.get('uuid')).update({
            'title': form.get('title', cls.title),  # if can't get title then will no change
            'content': form.get('content', cls.content),  # if can't get content then will no change
            # UTC GMT+00时间，需要加上8小时才是中国时间GMT+08
            'edit_date': datetime.strptime(form.get('edit_date'), '%Y-%m-%dT%H:%M:%S.%fZ'),
            'status': form.get('status', cls.status)  # if can't get content then will no change
        })
        try:
            db.session.commit()
            return True
        except Exception as e:
            print e

    @classmethod
    def get_article_by_uuid(cls, uuid, abort=True):
        # get article by query of uuid
        # write uuid judgement here,use re module as a practise
        # 0e3a6e0f-c720-11e6-852c-f4066974556c
        if abort:
            return cls.query.filter(cls.uuid == uuid, cls.status == 'PUBLISHED').first_or_404()
        else:
            # if use .one() method, will through NoResultFound error
            # use .first() method to return None if not existed
            return cls.query.filter(cls.uuid == uuid).first()

    @classmethod
    def latest_article(cls, page=1, author='scc'):
        # get articles which are in published status
        n = page * 5
        return cls.query. \
                   filter(cls.status == 'PUBLISHED', cls.author == author). \
                   order_by(desc(cls.create_date)). \
                   all()[n - 5:n]

    @classmethod
    def pagination(cls, page, author='scc'):
        # get paginate of query
        return cls.query.filter(cls.author == author).paginate(page, per_page=5, error_out=True)

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
                'title': 'NoResultFound',
                'description': 'NoResultFound',
                'done': False
            }

    @classmethod
    def status_ordered_list(cls, uuid=None):
        """
        返回一个以文章当前状态为首，并列出其余状态的有序字典。
        以供ArticleEditor.html页面进行调用
        :return:OrderedDict
        """
        rv = cls.query.filter(cls.uuid == uuid).first()
        constraint_total = {"PUBLISHED", "DRAFTED", "ARCHIVED",
                            "DELETED"}  # ==set(['DELETED', 'DRAFTED', 'ARCHIVED', 'PUBLISHED'])
        rs = constraint_total - {rv.status}
        return rs

    @classmethod
    def recent_articles(cls, author=None):
        rv = cls.query.filter(cls.author == author, cls.status == 'PUBLISHED'). \
            order_by(desc(cls.create_date)). \
            limit(5). \
            all()

        return rv

    @classmethod
    def categories(cls):
        pass

    @classmethod
    def get_published_article(cls, usr=None):
        rv = cls.query.filter(cls.status == "PUBLISHED", cls.author == usr).\
            order_by(desc(cls.create_date)).\
            all()
        return rv


class Comment(db.Model):
    """
    store the comments leaved by reader
    """
    # Comment.uid = Article.uuid it's not unique, do not use it to delete comments, use id instead
    __tablename__ = "Comment"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, unique=True)
    uid = db.Column(db.String(50), nullable=False)
    rdr_name = db.Column(db.String(20), nullable=False)
    rdr_mail = db.Column(db.String(20), nullable=False)
    rdr_message = db.Column(db.String(200), nullable=False)
    reply_id = db.Column(db.String(50), nullable=False, unique=True,
                         default=gen_uid)  # generate an random id for comment
    reply_to_id = db.Column(db.String(50), default=None, nullable=True)  # use id to indicate who reply to who
    message_date = db.Column(db.DATETIME, nullable=False, default=gen_dat)
    approved = db.Column(db.BOOLEAN, default=0, nullable=False)

    @classmethod
    def show_message(cls, uuid=None):
        """
        use WITH RECURSIVE expression to query the comments
        required version sqlite > 3.8.3
        find more at http://www.sqlite.org/lang_with.html.

        parent id : reply_to_id(root = NULL)
        child id : reply_id

        from root search every parent and his children, sort by parent time. two levels
        :param uuid:indicator of the unique article
        :return:nested object with query class
        """
        def nest(lst):
            """
            aim to turn flatten list (which fetched from sql) to nested structure
            :param lst: list
            :return: nested list
            """
            if not lst:
                return None
            first = lst[0]
            del lst[0]
            return {"pid": first, "id": nest(lst)}
        # @1:query all the unique reply_id of Comment order by time
        children_id_list = cls.query.filter(cls.uid == uuid, cls.approved == True). \
            order_by(desc(cls.message_date))
        # @2:use WITH RECURSIVE expression to query all the parent comments
        recursive_sql = text("""
          with recursive
            cte(id, reply_id, reply_to_id, rdr_mail, rdr_message, rdr_name, message_date) as (
              select id, reply_id, reply_to_id, rdr_mail, rdr_message, rdr_name ,message_date from Comment where reply_id = :a and approved = 1 and uid = :b
              union all
              select Comment.id, Comment.reply_id, Comment.reply_to_id, Comment.rdr_mail, Comment.rdr_message, Comment.rdr_name, Comment.message_date from Comment join cte on Comment.reply_id = cte.reply_to_id
              )
          select * from cte""")

        result = list()
        for _, child in enumerate(children_id_list):
            raw_sql = recursive_sql.bindparams(a=child.reply_id, b=uuid)
            rv = db.session.execute(raw_sql).fetchall()
            result.append(nest(rv))
        # @3:construct a nested list or generator for JinJa for loop recursive
        return result

    @staticmethod
    def approved_message():
        rv = db.session.query(Comment). \
            filter(Comment.approved == False). \
            order_by(desc(Comment.uid), desc(Comment.message_date)). \
            all()
        return rv

    @classmethod
    def del_message(cls, row_id=None):
        # use id to delete comments, do not use uid
        try:
            cls.query.filter(cls.id == row_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print e
            return False

    @classmethod
    def appr_message(cls, row_id=None):
        # use id to approve comments, do not use uid
        try:
            cls.query.filter(cls.id == row_id).update({"approved": True})
            db.session.commit()
            return True
        except Exception as e:
            print e
            return False

    @classmethod
    def recent_comments(cls, author=None):
        # union query will get two model objects at a list [(model object 1, model object 2), ...]
        rv = db.session.query(cls, Article). \
            outerjoin(Article, Article.uuid == cls.uid). \
            filter(cls.approved == True). \
            order_by(desc(cls.message_date)). \
            limit(5). \
            all()
        return rv


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

    def generate_auth_token(self, expiration=600):
        # 自己构造HTTP头Authorization: Basic 用BASE64加密"用户:密码"
        # 我们一直试着尽可能地坚持 HTTP 标准协议。既然我们需要实现认证我们需要在 HTTP 上下文中去完成，
        # HTTP 协议提供了两种认证机制: Basic 和 Digest。
        # HTTP 基本认证方式不特别要求 usernames 和 passwords 用于认证，
        # 在 HTTP 头中这两个字段可以用于任何类型的认证信息。基于令牌的认证，
        # 令牌可以作为 username 字段，password 字段可以忽略。
        s = TimedJSONWebSignatureSerializer(config['default'].SECRET_KEY, expires_in=expiration)
        return s.dumps({"id_": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(config['default'].SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = Login.query.get(data['id_'])
        return user

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
        # flask_login.login_user(user, remember=False, force=False, fresh=True)[source]
        # Logs a user in. You should pass the actual user object to this.
        # If the user’s is_active property is False, they will not be logged in unless force is True.
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
