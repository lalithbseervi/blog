from django.db import models
from mdeditor.fields import MDTextField
from django.urls import reverse

# Create your models here.
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    body = MDTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="blogposts")
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title
    
    def get_share_url(self):
        return reverse('share', kwargs={'token': self.share_token})