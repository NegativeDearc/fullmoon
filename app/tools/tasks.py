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
# caution1: celery 4.0 not support Windows anymore, use celery==3.1 instead
# caution2: RuntimeError: Running a worker with superuser privileges when the
# worker accepts messages serialized with pickle is a very bad idea!
# If you really want to continue then you have to set the C_FORCE_ROOT
# environment variable (but please think about this before you do).

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
            with app.app_context():
                mail.send(msg)
        except Exception as e:
            self.retry(exc=e, countdown=15, max_retries=5)
