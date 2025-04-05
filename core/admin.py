from django.contrib import admin
from django import forms
from django.db import models

# Register your models here.
from .models import BlogPost, Category

from tinymce.widgets import TinyMCE

class PostAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

    class Meta:
        model = BlogPost
        fields = '__all__'

@admin.register(BlogPost)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    
    list_display = ('title', 'share_token')

admin.site.register(Category)