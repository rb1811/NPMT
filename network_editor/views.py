from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    context = {'active_tab': 'network_editor'}
    return render(request, 'network_editor/index.html', context)