from django.urls import path
from .views import index, send_network_data

urlpatterns = [
    path('', index, name='index'),
    path('api/network-data/', send_network_data, name='send-network-data'),
]