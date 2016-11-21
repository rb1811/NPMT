from django.conf.urls import url, include

from . import views

app_name = 'network_editor'  # used in template as 'polls:detail' for eg.
urlpatterns = [
    # ex: /network_editor/
    url(r'^$', views.index, name='index'),
    url(r'^save$', views.save, name='save'),
]