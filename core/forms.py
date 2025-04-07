from django import forms
from .models import BlogPost, Category
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage

class FlatPageForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 50})}
        fields = ['content']

class BlogPostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=False 
    )

    class Meta:
        model = BlogPost
        fields = '__all__'