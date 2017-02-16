# coding:utf-8
from app import create_celery
from app import app
from app.models.database import mail
from celery import platforms
from smtplib import SMTPDataError

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
# solution: "celery -A app.tools.tasks.celery worker --loglevel=info" from the root
# caution1: celery 4.0 not support Windows anymore, use celery==3.1 instead
# caution2: RuntimeError: Running a worker with superuser privileges when the
# worker accepts messages serialized with pickle is a very bad idea!
# If you really want to continue then you have to set the C_FORCE_ROOT
# environment variable (but please think about this before you do).
#  nohup /root/Webapps/fullmoon/venv/bin/python
# /root/Webapps/fullmoon/venv/bin/celery -A app.tools.tasks.celery worker --loglevel=info > celery_nohup


@celery.task
def add_together(a, b):
    return a + b


# http://docs.celeryproject.org/en/latest/reference/celery.app.task.html?highlight=self.retry#celery.app.task.Task.retry
@celery.task(bind=True)
def send_mail(self, msg):
    debug = app.debug
    if debug:
        print("mail at debug model will not be sent!")
    else:
        try:
            # issue: I've already add task to app_context by create_celery function
            # why do I need to with app_context again?
            with app.app_context():
                mail.send(msg)
        except SMTPDataError as e:
            print("The SMTP server didn't accept the data, %s" % e)
        except Exception as e:
            self.retry(exc=e, countdown=30, max_retries=3)


@celery.task
def login_failed():
    # if someone trying to login to backend, but failed
    pass


@celery.task
def login_success():
    # if someone trying to login to backend, and succeed
    pass
