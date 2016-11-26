import json
from django.db import models
from scipy.spatial import ConvexHull
from helpers import coordinates_converter as conv


# Create your models here.
class FaultAnalyzer(models.Model):
    def analyze_generic(self, network_id, fault_radius):
        return {
            'composition_deposition_number': 1,
            'largest_component_size': 5,
            'smallest_component_size': 3,
            'fault_regions_considered': 2000,
            'rbcdn_faults': [{'x': 48.6909603909255, 'y': -11.337890625}, {'x': 54.3677585240684, 'y': -86.572265625}]
        }

    def generate_fault_region(self, nodes):
        nodes = conv.get_xy_for(nodes)
        points = [[node['x'], node['y']] for node in nodes]
        hull = ConvexHull(points)
        hull_xy = [{'x': points[vertex][0], 'y': points[vertex][1]} for vertex in hull.vertices]
        nodes = conv.get_lat_lng_for(hull_xy)
        return nodes
