import json
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_protect

from .models import Network


def index(request):
    context = {'active_tab': 'network_editor'}
    return render(request, 'network_editor/index.html', context)


@csrf_protect
def save(request):
    network = json.loads(request.body)
    context = {'active_tab': 'network_editor', 'network': network}
    Network.create_from_nodes_and_edges(network['name'], network['description'], network['nodes'], network['edges'])
    return JsonResponse(context)
