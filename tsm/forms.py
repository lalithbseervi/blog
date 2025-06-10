from django import forms
from .models import Node, Link

class NodeForm(forms.Form):
    class Meta:
        model = Node
        fields = ['id', 'rel']

class LinkForm(forms.Form):
    class Meta:
        model = Node
        fields = ['source', 'target']