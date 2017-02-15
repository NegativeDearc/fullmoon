# coding:utf-8
from app import create_celery
from app import app
from app.models.database import mail

celery = create_celery(app=app)


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
# caution: celery 4.0 not support Windows anymore, use celery==3.1 instead
@celery.task
def add_together(a, b):
    return a + b


@celery.task
def send_mail(self, msg, debug=app.debug):
    if debug:
        print("mail at debug model will not be sent!")
    else:
        try:
            mail.send(msg)
        except Exception as e:
            self.retry(exc=e, countdown=15, max_retries=5)
