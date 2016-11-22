from django.conf.urls import url, include

from . import views

app_name = 'network_editor'  # used in template as 'polls:detail' for eg.
urlpatterns = [
    # ex: /network_editor/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<network_id>[0-9]+)$', views.edit, name='edit'),
    url(r'^save$', views.save, name='save'),
    url(r'^udpate$', views.update, name='update'),
    url(r'^load', views.load, name='load'),
]