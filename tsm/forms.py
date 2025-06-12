from django import forms
from .models import Node, NodeAttribute, Link

class NodeForm(forms.ModelForm):
    id = forms.CharField(max_length=256, required=True)
    rel = forms.CharField(max_length=128, required=True)
    node_type = forms.CharField(required=True)

    class Meta:
        model = Node
        fields = '__all__'

class NodeAttrForm(forms.ModelForm):
    node = forms.ModelChoiceField(
        queryset=Node.objects.all(),
        required=True
    )

    key = forms.CharField(max_length=128, required=True)
    value_text = forms.CharField(required=False)
    value_int = forms.IntegerField(required=False)
    value_bool = forms.BooleanField(required=False)

    class Meta:
        model = NodeAttribute
        fields = '__all__'
        widgets = {
            'value_date': forms.DateInput(format=('%m-%d-%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class LinkForm(forms.ModelForm):
    source = forms.ModelChoiceField(
        queryset=Node.objects.all(),
        required=True
    )
    
    target = forms.ModelChoiceField(
        queryset=Node.objects.all(),
        required=True
    )

    class Meta:
        model = Link
        fields = '__all__'