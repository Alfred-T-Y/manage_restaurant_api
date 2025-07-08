import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manage_restaurant_api.settings")

app = Celery("manage_restaurant_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task
def add_numbers():
    return