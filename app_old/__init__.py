import os
from flask import Flask
from celery import Celery
from redis import Redis
from config import config, Config
from app.tasks import add

celery = Celery(__name__,
                broker=Config.CELERY_BROKER_URL,
                backend=Config.CELERY_RESULT_BACKEND)


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    celery.conf.update(app.config)

    record_tasks = Redis(host=app.config['REDIS_URL'])
    record_tasks = []

    @app.route('/')
    def hello_world():
        task_list = 'Task list: \n'
        for id in record_tasks:
            task = add.AsyncResult(id)
            task_list = task_list + f'{id}, state: {task.status}\n'

        new_task = add.apply_async()
        record_tasks.append(new_task.id)
        task_list = task_list + f'\n\nAdded new task, {new_task.id}'
        return '{}'.format(task_list)
        # return 'hello world'

    return app



