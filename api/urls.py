from django.urls import path
from . import views

urlpatterns = [
    path('incidents/active/', views.active_incidents, name='active_incidents'),
    path('metrics/latest/', views.latest_metrics, name='latest_metrics'),
]