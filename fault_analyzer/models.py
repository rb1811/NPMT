import json
from django.db import models
from scipy.spatial import ConvexHull
from helpers import coordinates_converter as conv
from helpers import analyzer

# Create your models here.
from network_editor.models import Network


class FaultAnalyzer(models.Model):
    def analyze_generic(self, network_id, fault_radius):
        network = Network.objects.get(pk=network_id)
        results = analyzer.analyze(network, fault_radius)
        return results


    def generate_fault_region(self, nodes):
        nodes = conv.get_xy_for(nodes)
        points = [[node['x'], node['y']] for node in nodes]
        hull = ConvexHull(points)
        hull_xy = [{'x': points[vertex][0], 'y': points[vertex][1]} for vertex in hull.vertices]
        nodes = conv.get_lat_lng_for(hull_xy)
        return nodes
