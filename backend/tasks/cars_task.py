import asyncio

from celery import Celery
from config import settings
from core.model_utils import update_cars_position_random

app = Celery(__name__, broker=settings.CELERY_BROKER_URL)
loop = asyncio.get_event_loop()


@app.task(name="update_cars_position")
def update_cars_position():
    try:
        loop.run_until_complete(update_cars_position_random())
    except:
        return "Error!"
    return "Cars position updated."


app.conf.beat_schedule = {
    "run-task-update-cars-position": {
        "task": "update_cars_position",
        "schedule": 180.0,
    },
}
