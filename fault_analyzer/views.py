from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'active_tab': 'fault_analyzer'}
    return render(request, 'fault_analyzer/index.html', context)
