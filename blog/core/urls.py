from django.urls import path
from . import views

urlpatterns = [
    path("", views.access, name="access"),
    path("home/", views.index, name="index"),
    path("posts/<int:pk>/", views.viewBlogByID, name="viewBlog"),
    path("posts/create/", views.create_post, name='createBlogPost'),
    path("posts/<int:pk>/edit/", views.edit_post, name='editBlogPost'),
    path("posts/<int:pk>/delete/", views.delete_post, name='deleteBlogPost'),
    path("posts/share/<uuid:token>/", views.share, name='share'),
    path("category/<str:category>/", views.viewBlogByCategory, name="viewBlogByCategory"),
]