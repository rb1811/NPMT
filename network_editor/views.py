import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_protect

from .models import Network


def index(request):
    context = {'active_tab': 'network_editor'}
    return render(request, 'network_editor/index.html', context)


@csrf_protect
def save(request):
    context = {"abc": 123}
    network = json.loads(request.body)
    Network.create_from_nodes_and_edges(network['name'], network['description'], network['nodes'], network['edges'])
    return render(request, 'network_editor/index.html', context)
