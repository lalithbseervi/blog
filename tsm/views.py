from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from .models import Node, Link
from .forms import NodeForm, NodeAttrForm, LinkForm
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
        return redirect('index')
    else:
        form = NodeForm()
    return render(request, 'tsm/forms/addNode.html', {'form': form})

def addNodeAttr(request):
    if request.method == 'POST':
        form = NodeAttrForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data['node']
            node = Node.objects.get(id=id)
            print(f"node_id: {node.id}")
            form.save()
        return redirect('profile', id=node.id)
    else:
        form = NodeAttrForm()
    return render(request, 'tsm/forms/addNodeAttr.html', {'form': form})

def addLink(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid:
            form.save()
        return redirect('index')
    else:
        form = LinkForm()
    return render(request, 'tsm/forms/addLink.html', {'form': form})

def serialize_network_data(request):
    nodes = []
    links = []

    total_nodes = Node.objects.prefetch_related('attributes')
    total_links = Link.objects.all()

    for node in total_nodes:
        node_dict = {
            "id": node.id,
            "rel": node.rel,
            "color": color(node),
            "marker": {
                "radius": radius(node),
                "symbol": symbol(node),
            },
            "rel_info": node.tooltip_info,
            "node_type": node.node_type
        }

        for attr in node.attributes.all():
            node_dict[attr.key] = attr.value()
        
        nodes.append(node_dict)

    for link in total_links:
        link_arr = [f'{link.source}', f'{link.target}']
        links.append(link_arr)
    
    return {
        "nodes": nodes,
        "links": links
    }

def radius(node):
    return 30 + node.attributes.count() * 5

def symbol(node):
    node_type = node.node_type

    symbol = {
        'apartment': 'diamond',
        'organization': 'square',
        # 'person': 'circle'
    }

    return symbol.get(node_type, 'circle')

def color(node):
    node_type = node.node_type

    colors = {
        'immediate_family': '#2caffe',
        'extended_family': '#2cbfff',
        'organization': 'red',
        'apartment': 'yellow'
    }

    return colors.get(node_type, 'grey')

def send_network_data(request):
    if request.user.is_superuser:
        data = serialize_network_data(request)
        return JsonResponse(data, safe=False)
    return HttpResponseServerError({'503 Service Unavailable'})