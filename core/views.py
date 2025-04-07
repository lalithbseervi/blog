from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from functools import wraps
from .utils import is_mobile_device, is_ajax, fetchQuote, BlogDetail, BlogPostService
import json

def superuser(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return error403(request, exception=HttpResponseForbidden)
        return view(request, *args, **kwargs)
    return _wrapped_view

def access(request):
    return render(request, 'core/terminal.html')

def fetch(request):
    codes = {
        '512800': {
            'template': 'core/111111.html',
            'context': {
                'name': 'Sir',
                'IP': request.META.get('HTTP_X_FORWARDED_FOR', 'N/A'),
                'u_agent': request.META.get('HTTP_USER_AGENT', 'N/A'),
            }
        },
    }

    code = request.GET.get('code_inp')

    if code in codes:
        template = codes[code]['template']
        context = codes[code]['context']
        return render(request, template, context)
    else:
        context = {
            'IP': request.META.get('HTTP_X_FORWARDED_FOR', 'N/A'),
        }
        return render(request, 'core/terminal.html', context)

def index(request):
    pageNo = request.GET.get('page')
    is_mobile = is_mobile_device(request)
    posts, paginator = BlogPostService.getPosts(request.user, pageNo, 5 if is_mobile else 6)
    quote = fetchQuote()

    context = {
        "posts": posts,
        "paginator": paginator,
        'quote': quote,
    }

    if is_ajax(request):
        posts = render_to_string('core/components/partial_posts.html', context)
        pagination = render_to_string('core/components/pagination.html', context)

        return JsonResponse({
            'posts': posts,
            'pagination': pagination,
        })

    response = render(request, 'core/index.html', context)
    return response

def viewBlogByCategory(request, category):
    pageNo = request.GET.get('page')
    posts = BlogPostService.getPostsByCategory(request.user, category, pageNo)
    quote = fetchQuote()

    context = {
        "category": category,
        "posts": posts,
        "quote": quote
    }

    return render(request, 'core/category.html', context)

def viewBlog(request, slug):
    post = BlogDetail.getBlogDetailAdminView(request, slug)
    related_posts = BlogPostService.getRelatedPosts(request.user, slug)
    quote = fetchQuote()

    context = {
        'post': post,
        'related_posts': related_posts,
        'quote': quote
    }

    if context == False:
        return render(request, 'core/404.html')
    else:
        return render(request, 'core/blogpost.html', context)

@superuser
def create_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)

        if form.is_valid():
            post = form.save()
        return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'core/create_post.html', {'form': form})

@superuser
def edit_post(request, slug):
    blogpost = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blogpost)
        if form.is_valid():
            form.save()
            return redirect('viewBlog', slug=blogpost.slug)
        else:
            form = BlogPostForm(instance=blogpost)
        return render(request, 'core/edit_post.html', {'form': form, 'blog_post': blogpost})
    form = BlogPostForm(instance=blogpost)
    return render(request, 'core/edit_post.html', {'form': form, 'blog_post': blogpost})

@superuser
def delete_post(slug):
    blogpost = get_object_or_404(BlogPost, slug=slug)
    blogpost.delete()
    return redirect('index')

def share(request, uuid):
    quote = fetchQuote()
    slug = BlogPost.objects.get(share_token=uuid).slug
    related_posts = BlogPostService.getRelatedPosts(request.user, slug)

    context = {
        'post': BlogDetail.getBlogDetailShareView(uuid),
        'quote': quote,
        'related_posts': related_posts
    }

    return render(request, 'core/share_blog.html', context)

def search(request):
    if request.method == 'POST':
        request_body = request.body.decode('utf-8')
        parsed_body = json.loads(request_body)
        query = parsed_body['search_query']

        posts = BlogPost.objects.filter(title__icontains=query) or BlogPost.objects.filter(Q(body__icontains=query)) or BlogPost.objects.filter(Q(categories__name__icontains=query))

        if not request.user.is_superuser:
            posts = posts.filter(password_protect=False)

        results = []
        for post in posts:
            post_data = {
                "title": post.title,
                "date_created_on": post.created_on.strftime('%b. %d, %Y'),
                "categories": [category.name for category in post.categories.all()],
                "slug": post.slug
            }
            results.append(post_data)

        return JsonResponse({'results': results})

    quote = fetchQuote()

    return render(request, 'core/components/search.html', {'quote': quote})

def error403(request, exception):
    return render(request, 'core/error/403.html')

def error404(request, exception):
    return render(request, 'core/error/404.html')