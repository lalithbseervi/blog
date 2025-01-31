from django.contrib import admin

# Register your models here.
from .models import BlogPost, Category

# class CategoryAdmin(admin.ModelAdmin):
#     pass

# class PostAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Category)
admin.site.register(BlogPost)