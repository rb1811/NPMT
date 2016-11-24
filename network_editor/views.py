import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
import HTMLParser
from django.views.decorators.csrf import csrf_protect
from django.core import serializers

from .models import Network


def index(request):
    context = {'active_tab': 'network_editor'}
    return render(request, 'network_editor/index.html', context)


@csrf_protect
def save(request):
    network = json.loads(request.body)
    network = Network.create_from_nodes_and_edges(network['name'], network['description'], network['nodes'],
                                                  network['edges'])
    url = reverse('network_editor:edit', args=[network.id])
    response = {'status': 1, 'message': "Network saved", 'redirect_url': url}
    return JsonResponse(response)


def load(request):
    networks = Network.objects.all()
    networks = serializers.serialize('json', networks, fields=('name', 'description'))
    data = {'networks': json.loads(networks)}
    return JsonResponse(data)


def create_node_list_json(nodes):
    node_list = [{'x': node.x, 'y': node.y} for node in nodes]
    return json.dumps(node_list)


def edit(request, network_id):
    network = Network.objects.get(pk=network_id)
    edges = network.edge_set.all()
    nodes = network.node_set.all()
    network_json = serializers.serialize('json', [network], fields=('name', 'description'))
    edges_json = create_edge_list_json(edges)
    nodes_json = create_node_list_json(nodes)
    network_json = HTMLParser.HTMLParser().unescape(network_json)
    context = {'active_tab': 'network_editor',
               'mode': 'edit',
               'network': network_json,
               'nodes': nodes_json,
               'edges': edges_json,
               'network_id': network_id}
    return render(request, 'network_editor/index.html', context)


def create_edge_list_json(edges):
    edge_list = [
        {'start_node': {'x': e.start_node.x, 'y': e.start_node.y}, 'end_node': {'x': e.end_node.x, 'y': e.end_node.y}}
        for e in edges]
    return json.dumps(edge_list)


def update(request):
    network = json.loads(request.body)
    Network.update_from_nodes_and_edges(network['id'], network['name'], network['description'], network['nodes'],
                                        network['edges'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
