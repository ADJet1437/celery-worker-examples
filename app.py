import logging
from time import sleep
from celery import Celery

logger = logging.getLogger(__name__)
QUEUE_RATE_LIMIT = '10/s'

worker = Celery('worker', broker='pyamqp://admin:admin@rabbitmq:5672/admin')
worker.conf.task_routes = {
    'app.simple_single_task': {'queue': 'queue_for_simple_single_task_worker'}
}


@worker.task()
def simple_periodic_task():
    """A regular task scheduled every second
    """
    logger.info('Starting ...')
    sleep(1)
    logger.info('Finished!')


@worker.task(bind=True, rate_limit=QUEUE_RATE_LIMIT)
def simple_task_with_rate_limit(*args):
    """This task is scheduled every second, due to the rate limit, it will be
    consumed every 10 seconds
    """
    logger.info('Work starting ...')
    print(*args)
    logger.info('Work finished!')


@worker.task()
def simple_single_task():
    """Some specific reason that want to run this task in a separate worker"""
    logger.info('Starting ...')
    sleep(1)
    logger.info('Finished!')


@worker.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print(kwargs)
    sender.add_periodic_task(1, simple_periodic_task.s(), name='Every second')
    sender.add_periodic_task(1, simple_task_with_rate_limit.s(), name='Every second')
    sender.add_periodic_task(1, simple_single_task.s(), name='Single worker every every')
