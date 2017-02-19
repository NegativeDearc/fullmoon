# coding:utf-8
from app import create_celery
from app import app
from app.models.database import mail
from app.models.model import Article, db
from celery import platforms
from smtplib import SMTPDataError
from flask.ext.mail import Message

celery = create_celery(app=app)
platforms.C_FORCE_ROOT = True  # or export C_FORCE_ROOT="true" at linux


# how to run the celery process?
# this file named tasks.py
# active your (virtual) environment
# cd the directory with the tasks.py
# command "python -m celery -A tasks.celery worker --loglevel=info"
# or "celery -A tasks.celery worker --loglevel=info"
# in Linux "venv/bin/celery worker -A tasks.celery --loglevel=info" is ok too
# before we run the app, we must run the celery process first.
# issue[fixed] :"ImportError: No module named app"
# solution: "celery worker -A app.tools.tasks.celery --loglevel=info" from the root
# caution1: celery 4.0 not support Windows anymore, use celery==3.1 instead
# caution2: RuntimeError: Running a worker with superuser privileges when the
# worker accepts messages serialized with pickle is a very bad idea!
# If you really want to continue then you have to set the C_FORCE_ROOT
# environment variable (but please think about this before you do).
#  nohup /root/Webapps/fullmoon/venv/bin/python
# /root/Webapps/fullmoon/venv/bin/celery -A app.tools.tasks.celery worker --loglevel=info > celery_nohup
# http://docs.celeryproject.org/en/latest/reference/celery.app.task.html?highlight=self.retry#celery.app.task.Task.retry
# issue: have problems execute tasks in linux, maybe the problem of serialization
# try to change to JSON, instead of pickle
@celery.task(bind=True, max_retries=3, default_retry_delay=60*0.5, track_started=True)
def send_mail(self, raw_msg):
    debug = app.debug
    if debug:
        print("mail at debug model will not be sent!")
    else:
        try:
            # issue: I've already add task to app_context by create_celery function
            # why do I need to with app_context again?
            print(raw_msg)
            with app.app_context():
                msg = Message(subject=raw_msg["subject"], recipients=raw_msg["recipients"])
                msg.html = raw_msg["html"]
                mail.send(msg)
        except SMTPDataError as e:
            print("The SMTP server didn't accept the data, %s" % e)
        except Exception as e:
            self.retry(exc=e)


@celery.task
def login_failed():
    # if someone trying to login to backend, but failed
    pass


@celery.task
def login_success():
    # if someone trying to login to backend, and succeed
    pass


@celery.task
def add_read_times(uuid=None):
    rv = db.session.query(Article).filter(Article.uuid == uuid).one()
    if isinstance(rv.read_times, int):
        rv.read_times += 1
    else:
        rv.read_times = 0
    db.session.commit()
