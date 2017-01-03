from celery import Celery

from exellentodb import Excellentodb



celery_app = Celery(__file__, 'redis://localhost:6379/0')



@celery_app.task
def process_file(filename):
    return Excellentodb(filename).toexcel()