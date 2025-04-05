from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Category
from .forms import BlogPostForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from functools import wraps
from .utils import is_mobile_device, is_ajax, fetchQuote

# Create your views here.
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

class BlogPostService:
    @staticmethod
    def getPosts(user: User, pageNo: int, number_of_posts: int) -> list:
        if user.is_superuser:
            posts = BlogPost.objects.all()
        else:
            posts = BlogPost.objects.all().filter(password_protect=False)

        paginatorInstance = Paginator(posts, number_of_posts)

        try:
            postsPage = paginatorInstance.get_page(pageNo)
        except PageNotAnInteger:
            postsPage = paginatorInstance.get_page(1)
        except EmptyPage:
            postsPage = paginatorInstance.get_page(paginatorInstance.num_pages)
            postsPage.adjusted_elided_pages = paginatorInstance.get_elided_page_range(pageNo)
        return postsPage, paginatorInstance

    @staticmethod
    def getPostsByCategory(user: User, category: Category, pageNo) -> list:
        if user.is_superuser:
            posts = BlogPost.objects.filter(Q(categories__name__icontains=category))
        else:
            posts = BlogPost.objects.filter(Q(categories__name__icontains=category) & Q(password_protect=False))

        paginatorInstance = Paginator(posts, 4)

        try:
            postsPage = paginatorInstance.get_page(pageNo)
        except PageNotAnInteger:
            postsPage = paginatorInstance.get_page(1)
        except EmptyPage:
            postsPage = paginatorInstance.get_page(paginatorInstance.num_pages)
            postsPage.adjusted_elided_pages = paginatorInstance.get_elided_page_range(pageNo)
        return postsPage

    @staticmethod
    def getRelatedPosts(user: User, slug) -> list:
        post = get_object_or_404(BlogPost, slug=slug)
        categories = post.categories.all()

        for category in categories:
            related_posts = BlogPost.objects.filter(categories=category).exclude(slug=slug)

        if user.is_superuser is False:
            related_posts.filter(password_protect=False)

        return related_posts

class BlogDetail:
    @staticmethod
    def getBlogDetailAdminView(request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        if post.password_protect:
            if request.user.is_superuser:
                pass
            else:
                return error403(request, exception=HttpResponseForbidden)
        response = {
            'title': post.title,
            'share_link': post.get_share_url(),
            'categories': post.categories.all(),
            'created_on': post.created_on,
            'last_modified': post.last_modified,
            'body': post.body,
            'slug': post.slug,
            'req_toc': post.require_table_of_contents
        }
        return response

    @staticmethod
    def getBlogDetailShareView(uuid):
        post = get_object_or_404(BlogPost, share_token=uuid)

        response = {
            'title': post.title,
            'categories': post.categories.all(),
            'created_on': post.created_on.date,
            'last_modified': post.last_modified,
            'body': post.body,
            'req_toc': post.require_table_of_contents
        }

        return response

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

    ajax = is_ajax(request)

    if ajax:
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

    context = {
        "category": category,
        "posts": posts,
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

def error403(request, exception):
    return render(request, 'core/error/403.html')

def error404(request, exception):
    return render(request, 'core/error/404.html')