from .models import Node, Link

def serialize_network_data(request):
    total_nodes = Node.objects.prefetch_related('attributes')
    total_links = Link.objects.all()

    data = construct_dict(total_nodes, total_links)
    
    return {
        "nodes": data["nodes"],
        "links": data["links"]
    }

def construct_dict(nodes, links):
    constructed_nodes = []
    constructed_links = []

    for node in nodes:
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
        
        constructed_nodes.append(node_dict)

    for link in links:
        link_arr = [f'{link.source}', f'{link.target}']
        constructed_links.append(link_arr)
    
    constructed_data = {
        "nodes": constructed_nodes,
        "links": constructed_links
    }

    return constructed_data

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