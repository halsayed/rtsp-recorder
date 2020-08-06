from . import celery


@celery.task
def add(x=5, y=5):
    return x + y