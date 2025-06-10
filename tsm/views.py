from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden

from .models import Node, Link

# Create your views here.
def index(request):
    key = request.GET.get('key')
    cmp_key = '1121'

    if key != cmp_key:
        return HttpResponseForbidden("Page does not exist :(")
    
    return render(request, 'tsm/index.html')

def serialize_network_data(request):
    nodes = []
    links = []

    total_nodes = Node.objects.prefetch_related('attributes')
    total_links = Link.objects.all()

    for node in total_nodes:
        node_dict = {
            "id": node.id,
            "rel": node.rel,
            "marker": {
                "radius": radius(node)
            },
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
    return 25 + node.attributes.count() * 5

def send_network_data(request):
    data = serialize_network_data(request)
    return JsonResponse(data, safe=False)