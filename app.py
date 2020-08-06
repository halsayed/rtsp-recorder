import os
from time import time
from flask import Flask, jsonify
from flask_restx import Api, Resource
from redis import Redis
from celery import Celery
from config import config


app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV') or 'default'])
api = Api(app)

# Initialize Celery
celery = Celery(app.name,
                broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

record_tasks = Redis()
record_tasks = []


from tasks import add


@api.route('/capture')
class CaptureStream(Resource):
    def get(self):
        trigger_time = int(time())  # convert to int to drop microseconds
        before_buffer = 10
        after_buffer = 30
        new_task = add.apply_async(args=(trigger_time, before_buffer, after_buffer), countdown=after_buffer)
        record_tasks.append(new_task.id)

        return {'new_task': new_task.id}


@api.route('/tasks', '/task')
class Tasks(Resource):
    def get(self):
        task_list = []
        for task_id in record_tasks:
            task = add.AsyncResult(task_id)
            task_list.append({'id': task_id, 'state': task.status})

        return task_list


@api.route('/task/<string:task_id>')
class Task(Resource):
    def get(self, task_id):
        if task_id in record_tasks:
            task = add.AsyncResult(task_id)
            result = {
                'id': task.id,
                'state': task.state,
                'status': task.status,
                'result': task.result
            }
            return result
        else:
            return {'error': 'Task id not found'}, 500


if __name__ == '__main__':
    app.run()
