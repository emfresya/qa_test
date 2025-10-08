import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring_systems.settings')

app = Celery('monitoring_systems')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()