from app import celery
from datetime import datetime


@celery.task
def add(trigger_time, before_buffer, after_buffer):
    result = {
        'trigger_time': datetime.utcfromtimestamp(trigger_time).isoformat()+'Z',
        'before_buffer': before_buffer,
        'after_buffer': after_buffer
    }
    return result