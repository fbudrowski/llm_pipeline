from celery import Celery
from api.celery_config import make_celery
import time

celery = make_celery()

batch_data = []
# batch_size = 4


@celery.task
def collect_data(data_batch: list[str]):
    print(f"Got data {data_batch}")

    # Simulate data processing with a delay
    time.sleep(2)
    result = tuple(data.upper() for data in data_batch)
    print(f"Result: {result}")
    return result

    # global batch_data
    # batch_data.extend(data)
    # if len(batch_data) >= batch_size:
    #     result = process_batch(batch_data.copy())
    #     batch_data.clear()
    #     return result
    # else:
    #     while len(batch_data) < batch_size:
    #         time.sleep(0.1)
    #     result = process_batch(batch_data.copy())
    #     batch_data.clear()
    #     return result


