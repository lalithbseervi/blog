from django import forms
from mdeditor.fields import MDTextFormField, MDTextField
from .models import BlogPost, Category
from ckeditor.widgets import CKEditorWidget

# class createBlogPost(forms.Form):
#     title = forms.CharField()
#     body = MDTextFormField()
#     categories = forms.CheckboxSelectMultiple(choices=category_choices)

# class BlogPostForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'body', 'categories']
#         categories = forms.ChoiceField(choices=BlogPost.CategoryChoices.choices, widget=forms.Select())

class BlogPostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This renders checkboxes for multiple selections
        required=False  # You can make it required or optional depending on your needs
    )

    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BlogPost
        fields = '__all__'