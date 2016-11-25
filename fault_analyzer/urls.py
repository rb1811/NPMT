from django.conf.urls import url, include

from . import views

app_name = 'fault_analyzer'  # used in template as 'polls:detail' for eg.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^analyze$', views.analyze, name='analyze'),
    url(r'^analyze_fault_network', views.analyze_fault_network, name='analyze_fault_network'),
    url(r'^fault_region', views.fault_region, name='fault_region'),
    url(r'^(?P<network_id>[0-9]+)$', views.edit, name='edit'),
]
