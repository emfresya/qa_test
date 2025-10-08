from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    endpoint_url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Metric(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    cpu = models.FloatField()
    mem = models.FloatField()  # храним как число: 30.0
    disk = models.FloatField()
    uptime = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['machine', 'timestamp']),
        ]

class Incident(models.Model):
    INCIDENT_TYPES = [
        ('cpu', 'CPU Overload'),
        ('mem', 'Memory Overload'),
        ('disk', 'Disk Full'),
    ]

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=10, choices=INCIDENT_TYPES)
    started_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['machine', 'incident_type', 'is_active']),
        ]