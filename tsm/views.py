from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.template.loader import render_to_string

from .models import Node, Link
from .forms import NodeForm, NodeAttrForm, LinkForm
from .utils import serialize_network_data
from core.utils import is_ajax
import json
# Create your views here.
def index(request):
    return render(request, 'tsm/index.html')

def profile(request, id):
    id = request.GET.get('id') or id

    node = Node.objects.get(id=id)
    rel = node.tooltip_info
    attributes = node.attributes.all()

    return render(request, 'tsm/profile.html', context = { 'name': id, 'rel': rel, 'attributes': attributes })

def addNode(request):
    if request.method == "POST":
        form = NodeForm(request.POST)

        if form.is_valid():
            post = form.save()
            return HttpResponse(status=204)
        # return redirect('index')
    else:
        form = NodeForm()
        if is_ajax(request):
            form = render_to_string('tsm/forms/addNode.html', {'form': form}, request=request)
            return JsonResponse({'form': form})
    return render(request, 'tsm/forms/addNode.html', {'form': form})

def addNodeAttr(request):
    if request.method == 'POST':
        form = NodeAttrForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['node']
            node = Node.objects.get(id=id)
            print(f"node_id: {node.id}")
            form.save()
            return HttpResponse(status=204)
        # return redirect('profile', id=node.id)
    else:
        form = NodeAttrForm()
        if is_ajax(request):
            form = render_to_string('tsm/forms/addNodeAttr.html', {'form': form}, request=request)
            return JsonResponse({'form': form})
    return render(request, 'tsm/forms/addNodeAttr.html', {'form': form})

def addLink(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid:
            form.save()
            return HttpResponse(status=204)
        # return redirect('index')
    else:
        form = LinkForm()
        if is_ajax(request):
            form = render_to_string('tsm/forms/addLink.html', {'form': form}, request=request)
            return JsonResponse({'form': form})
    return render(request, 'tsm/forms/addLink.html', {'form': form})

## API Definitions

def send_network_data(request, *args):
    '''
        API definition to send serialised network graph data (nodes, node attributes, and links)
    '''
    if request.user.is_superuser:
        data = serialize_network_data(request)
        return JsonResponse(data, safe=False)
    return HttpResponseServerError({'503 Service Unavailable'})