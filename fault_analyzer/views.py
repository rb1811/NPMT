from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

import json
import HTMLParser

# Create your views here.
from fault_analyzer.models import FaultAnalyzer
from network_editor.models import Network


def index(request):
    context = {'active_tab': 'fault_analyzer'}
    return render(request, 'fault_analyzer/index.html', context)


def create_node_list_json(nodes):
    node_list = [{'x': node.x, 'y': node.y} for node in nodes]
    return json.dumps(node_list)


def create_edge_list_json(edges):
    edge_list = [
        {'start_node': {'x': e.start_node.x, 'y': e.start_node.y}, 'end_node': {'x': e.end_node.x, 'y': e.end_node.y}}
        for e in edges]
    return json.dumps(edge_list)


def edit(request, network_id):
    network = Network.objects.get(pk=network_id)
    edges = network.edge_set.all()
    nodes = network.node_set.all()
    network_json = serializers.serialize('json', [network], fields=('name', 'description'))
    edges_json = create_edge_list_json(edges)
    nodes_json = create_node_list_json(nodes)
    network_json = HTMLParser.HTMLParser().unescape(network_json)
    context = {'active_tab': 'fault_analyzer',
               'mode': 'edit',
               'network': network_json,
               'nodes': nodes_json,
               'edges': edges_json,
               'network_id': network_id}
    return render(request, 'fault_analyzer/index.html', context)


@csrf_protect
def analyze(request):
    data = json.loads(request.body)
    results = FaultAnalyzer().analyze_generic(data['network_id'], data['fault_radius'])
    response = {'status': 1, 'message': "Network Analyzed", 'results': results}
    return JsonResponse(response)


@csrf_protect
def fault_region(request):
    data = json.loads(request.body)
    fault_region_nodes = FaultAnalyzer().generate_fault_region(data['nodes'])
    response = {'status': 1, 'message': "Fault Region", 'nodes': fault_region_nodes}
    return JsonResponse(response)
