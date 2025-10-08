import requests
from celery import shared_task
from .models import Machine, Metric, Incident
from django.utils import timezone
from datetime import timedelta
from monitoring_systems.config import THRESHOLDS

@shared_task
def poll_machine(machine_id):
    try:
        machine = Machine.objects.get(id=machine_id)
        resp = requests.get(machine.endpoint_url, timeout=10)
        data = resp.json()

        # Преобразуем mem и disk в float
        mem = float(data['mem'].rstrip('%'))
        disk = float(data['disk'].rstrip('%'))

        metric = Metric.objects.create(
            machine=machine,
            cpu=data['cpu'],
            mem=mem,
            disk=disk,
            uptime=data['uptime']
        )

        check_incidents(metric)

    except Exception as e:
        print(f"Error polling machine {machine_id}: {e}")

@shared_task
def poll_all_machines():
    for machine in Machine.objects.all():
        poll_machine.delay(machine.id)

def check_incidents(metric):
    thresholds = THRESHOLDS

    # CPU: мгновенное превышение
    if metric.cpu > thresholds['cpu']:
        create_incident_if_not_exists(metric.machine, 'cpu')

    # MEM: >90% в течение 30 минут
    since = timezone.now() - timedelta(minutes=thresholds['mem_duration_minutes'])
    mem_high = Metric.objects.filter(
        machine=metric.machine,
        mem__gt=thresholds['mem'],
        timestamp__gte=since
    ).count()
    if mem_high >= 2:  # минимум 2 замера за 30 мин (каждые 15 мин → 2)
        create_incident_if_not_exists(metric.machine, 'mem')

    # DISK: >95% в течение 2 часов
    since = timezone.now() - timedelta(minutes=thresholds['disk_duration_minutes'])
    disk_high = Metric.objects.filter(
        machine=metric.machine,
        disk__gt=thresholds['disk'],
        timestamp__gte=since
    ).count()
    if disk_high >= 8:  # 8 замеров за 2 часа (каждые 15 мин)
        create_incident_if_not_exists(metric.machine, 'disk')

def create_incident_if_not_exists(machine, incident_type):
    if not Incident.objects.filter(
        machine=machine,
        incident_type=incident_type,
        is_active=True
    ).exists():
        Incident.objects.create(machine=machine, incident_type=incident_type)