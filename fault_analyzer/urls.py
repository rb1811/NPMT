from django.conf.urls import url, include

from . import views

app_name = 'fault_analyzer'  # used in template as 'polls:detail' for eg.
urlpatterns = [
    url(r'^$', views.index, name='index')
]