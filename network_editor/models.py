from __future__ import unicode_literals
from django.db import models
import datetime
import numpy
from django.utils import timezone


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

    @classmethod
    def create_from_nodes_and_edges(cls, name, description, nodes, edges):
        network = cls(name=name, description=description)
        network.save()
        for node in nodes:
            print node
            n = Node(x=numpy.float(node['lat']), y=numpy.float(node['lng']))
            try:
                n.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))

        for edge in edges:
            start = Node.objects.filter(x=edge['start']['lat'], y=edge['start']['lng'])[0]
            end = Node.objects.filter(x=edge['end']['lat'], y=edge['end']['lng'])[0]
            ed = Edge(network=network, start_node=start, end_node=end)
            try:
                ed.save()
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))


class Edge(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    start_node = models.ForeignKey(Node, related_name='start_node', default=None)
    end_node = models.ForeignKey(Node, related_name='end_node', default=None)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Edge, self).save(*args, **kwargs)
