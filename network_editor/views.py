import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
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
    Network.create_from_nodes_and_edges(network['name'], network['description'], network['nodes'], network['edges'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def load(request):
    networks = Network.objects.all()
    networks = serializers.serialize('json', networks, fields=('name', 'description'))
    data = {'networks': json.loads(networks)}
    return JsonResponse(data)


def edit(request, network_id):
    network = Network.objects.get(pk=network_id)
    edges = network.edge_set.all()
    network_json = serializers.serialize('json', [network], fields=('name', 'description'))
    edges_list = [
        {'start_node': {'x': e.start_node.x, 'y': e.start_node.y}, 'end_node': {'x': e.end_node.x, 'y': e.end_node.y}}
        for e in edges]
    edges_json = json.dumps(edges_list)
    network_json = HTMLParser.HTMLParser().unescape(network_json)
    context = {'active_tab': 'network_editor', 'mode': 'edit', 'network': network_json, 'edges': edges_json,
               'network_id': network_id}
    return render(request, 'network_editor/index.html', context)


def update(request):
    network = json.loads(request.body)
    Network.update_from_nodes_and_edges(network['id'], network['name'], network['description'], network['nodes'],
                                        network['edges'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
