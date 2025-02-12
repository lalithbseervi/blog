from django.contrib import admin

# Register your models here.
from .models import BlogPost, Category

from django import forms
from django.db import models
from ckeditor.widgets import CKEditorWidget

# from django.contrib.flatpages.admin import FlatPageAdmin
# from django.contrib.flatpages.models import FlatPage
# from django.utils.translation import gettext_lazy as _

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

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    prepopulated_fields = {"slug": "title"}

admin.site.register(Category)
admin.site.register(BlogPost)