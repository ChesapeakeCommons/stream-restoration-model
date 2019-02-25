#!/usr/bin/env python

# Import third-party dependencies

from celery import Celery

# Import package dependencies

from app import application


def make_celery(app):

    celery = Celery(app.import_name,
                    backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER'])

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):

        abstract = True

        def __call__(self, *args, **kwargs):

            with app.app_context():

                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


instance = application.Application(
    name=__name__,
    environment='development.DevelopmentConfig'
)

celery = make_celery(instance.app)
