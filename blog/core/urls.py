from django.urls import path
from . import views

urlpatterns = [
    path("", views.access, name='access'),
    path("home/", views.index, name='index'),
    path('fetch/', views.fetch, name='fetch'),
    path("category/<str:category>/", views.viewBlogByCategory, name="viewBlogByCategory"),
    path("posts/create/", views.create_post, name='createBlogPost'),
    path("posts/<slug:slug>/", views.viewBlog, name='viewBlog'),
    path("posts/<slug:slug>/download/", views.serve_pdf, name='downloadPDF'),
    path("posts/<slug:slug>/edit/", views.edit_post, name='editBlogPost'),
    path("posts/<slug:slug>/delete/", views.delete_post, name='deleteBlogPost'),
    path("posts/share/<uuid:uuid>/", views.share, name='share'),
]