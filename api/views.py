from django.shortcuts import render
from django.http import JsonResponse
from monitoring.models import Incident, Metric, Machine
from django.core.serializers import serialize
import json

def active_incidents(request):
    incidents = Incident.objects.filter(is_active=True).select_related('machine')
    data = [{
        'id': i.id,
        'machine': i.machine.name,
        'type': i.get_incident_type_display(),
        'started_at': i.started_at.isoformat(),
    } for i in incidents]
    return JsonResponse(data, safe=False)

def latest_metrics(request):
    metrics = []
    for machine in Machine.objects.all():
        latest = Metric.objects.filter(machine=machine).order_by('-timestamp').first()
        if latest:
            metrics.append({
                'machine': machine.name,
                'cpu': latest.cpu,
                'mem': latest.mem,
                'disk': latest.disk,
                'status': get_status(latest),
            })
    return JsonResponse(metrics, safe=False)

def get_status(metric):
    from monitoring_systems.config import THRESHOLDS as T
    if metric.cpu > T['cpu'] or metric.mem > T['mem'] or metric.disk > T['disk']:
        return 'critical'
    return 'ok'