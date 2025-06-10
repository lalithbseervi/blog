from django.contrib import admin
from .models import Node, Link, NodeAttribute

admin.site.register(Node)
admin.site.register(Link)
admin.site.register(NodeAttribute)