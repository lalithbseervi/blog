from django.db import models
from tinymce import models as tinymce_models
from django.urls import reverse
from django.utils.text import slugify
from django.test import Client

# Create your models here.
import uuid, weasyprint

from simple_history.models import HistoricalRecords

choices = {
    True: 'true',
    False: 'false'
}

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    body = tinymce_models.HTMLField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="blogposts", default=None)
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    password_protect = models.BooleanField(default=False, choices=choices, blank=True, null=True)
    require_table_of_contents = models.BooleanField(default=False, choices=choices, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-last_modified']

    def __str__(self):
        return self.title

    def get_share_url(self):
        return reverse('share', kwargs={'uuid': self.share_token})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def save_as_pdf(self) -> bytes:
        url = reverse('viewBlog', kwargs={'slug': self.slug})

        client = Client()
        client.login(username='lalith', password='dCRQu2!!??')

        html = client.get(url).content.decode('utf-8')

        css = weasyprint.CSS('https://devspace.pythonanywhere.com/static/simplePDF.css')

        pdf = weasyprint.HTML(string=html).write_pdf(stylesheets=[css])

        response = HttpResponse(pdf)
        response['Content-Disposition'] = f'attachment; filename="{self.title}.pdf"'

        return response