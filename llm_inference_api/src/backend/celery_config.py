from celery import Celery

from backend.tasks import BatchProcessing


def make_celery(app_name=__name__):
    return Celery(
        app_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )

celery = make_celery()
celery.conf.update(
    worker_concurrency=1,  # Number of threads per worker process
    task_always_eager=False,
    worker_pool='threads'
)

BatchProcessing = celery.register_task(BatchProcessing())