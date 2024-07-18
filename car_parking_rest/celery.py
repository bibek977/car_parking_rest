import os
from celery import Celery
from celery import shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_parking_rest.settings')

app = Celery('car_parking_rest')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()