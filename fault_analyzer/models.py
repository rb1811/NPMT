from django.db import models


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
