from django.urls import path
from .views import index, profile, send_network_data

urlpatterns = [
    path('', index, name='index'),
    path('profile', profile, name='profile'),
    path('api/network-data/', send_network_data, name='send-network-data'),
]