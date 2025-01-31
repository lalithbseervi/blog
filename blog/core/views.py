from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Category
from .forms import BlogPostForm
# Create your views here.

def access(request):
    return render(request, 'core/terminal.html')

"""List all the blog posts on the homepage."""
def index(request):
    code = request.GET.get('ref')
    if code == '512800' or request.COOKIES.get('invalid') == 'false':
        posts = BlogPost.objects.all().order_by("-created_on")
        response = render(request, 'core/index.html', {"posts": posts})
        response.set_cookie('invalid', 'false')
        return response
    else:
        response = render(request, 'core/404.html')
        response.set_cookie('invalid', 'true')
        return response

"""Find posts by category"""
def viewBlogByCategory(request, category):
    cookie = request.COOKIES.get('invalid')

    if cookie == 'true':
        render(request, 'core/404.html')

    posts = BlogPost.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, 'core/category.html', context)

"""View particular blog post"""
def viewBlogByID(request, pk):
    cookie = request.COOKIES.get('invalid')
    if cookie == 'true':
        render(request, 'core/404.html')
    
    blogpost = BlogPost.objects.get(pk=pk)
    context = {
        'title': blogpost.title,
        'share_link': blogpost.get_share_url(),
        'categories': blogpost.categories.all(),
        'created_on': blogpost.created_on.date,
        'body': blogpost.body,
        'pk': blogpost.pk
    }
    return render(request, 'core/blogpost.html', context)

def create_post(request):
    cookie = request.COOKIES.get('invalid')
    if cookie == 'true':
        render(request, 'core/404.html')
    if request.method == "POST":
        form = BlogPostForm(request.POST)

        if form.is_valid():
            post = form.save()
        return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'core/create_post.html', {'form': form})

def edit_post(request, pk):
    blogpost = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blogpost)
        if form.is_valid():
            form.save()  
            return redirect('viewBlog', pk=blogpost.id)  
    else:
        form = BlogPostForm(instance=blogpost)
    return render(request, 'core/edit_post.html', {'form': form, 'blog_post': blogpost})

def delete_post(request, pk):
    blogpost = get_object_or_404(BlogPost, pk=pk)
    blogpost.delete()
    return redirect('index')

def share(request, token):
    blogpost = get_object_or_404(BlogPost, share_token=token)
    context = {
        'title': blogpost.title,
        'categories': blogpost.categories.all(),
        'created_on': blogpost.created_on.date,
        'body': blogpost.body,
    }
    return render(request, 'core/share_blog.html', context)