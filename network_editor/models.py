from __future__ import unicode_literals
from django.db import models
from time import timezone


class Network(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(default="")
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Network, self).save(*args, **kwargs)


class Node(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Node, self).save(*args, **kwargs)


class Edge(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    start_node = models.OneToOneField(Node, related_name='start_node', default=None)
    end_node = models.OneToOneField(Node, related_name='end_node', default=None)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Edge, self).save(*args, **kwargs)
