from __future__ import print_function
from __future__ import print_function
from __future__ import unicode_literals
from django.db import models
import datetime
import numpy
from django.utils import timezone


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

    def update(self, name, description):
        self.name = name
        self.description = description
        self.save()

    def delete_edges_and_nodes(self):
        try:
            [e.delete() for e in self.edge_set.all()]
            [n.delete() for n in self.node_set.all()]
        except Exception as e:
            print('%s (%s)' % (e.message, type(e)))

    def add_nodes_and_edges(self, edges, nodes):
        for node in nodes:
            n = Node(x=numpy.float(node['lat']), y=numpy.float(node['lng']), network=self)
            try:
                n.save()
            except Exception as e:
                print('%s (%s)' % (e.message, type(e)))

        for edge in edges:
            start = Node.objects.filter(x=edge['start']['lat'], y=edge['start']['lng'])[0]
            end = Node.objects.filter(x=edge['end']['lat'], y=edge['end']['lng'])[0]
            ed = Edge(network=self, start_node=start, end_node=end)
            try:
                ed.save()
            except Exception as e:
                print('%s (%s)' % (e.message, type(e)))

    @classmethod
    def update_from_nodes_and_edges(cls, nId, name, description, nodes, edges):
        network = cls.objects.get(pk=nId)
        network.update(name=name, description=description)
        network.delete_edges_and_nodes()
        network.add_nodes_and_edges(edges=edges, nodes=nodes)

    @classmethod
    def create_from_nodes_and_edges(cls, name, description, nodes, edges):
        network = cls(name=name, description=description)
        network.save()
        network.add_nodes_and_edges(edges=edges, nodes=nodes)
        return network


class Node(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
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

    def delete(self, using=None):
        self.start_node.delete()
        self.end_node.delete()
        return super(Edge, self).delete()
