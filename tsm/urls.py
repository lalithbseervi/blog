from django.urls import path
from .views import index, profile, addNode, addNodeAttr, addLink, send_network_data

urlpatterns = [
    path('', index, name='index'),
    path('profile/<str:id>', profile, name='profile'),
    path('add_node', addNode, name='add_node'),
    path('add_link', addLink, name='add_link'),
    path('add_node_attr', addNodeAttr, name='add_node_attr'),
    path('api/network-data/', send_network_data, name='send-network-data'),
]