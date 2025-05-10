from django.http import HttpRequest
import random
from .models import BlogPost, Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

def is_mobile_device(request: HttpRequest) -> bool:
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        mobile_keywords = ['iphone', 'android', 'windows phone', 'mobile', 'blackberry', 'ipad']
        return any(keyword in user_agent for keyword in mobile_keywords)

def is_ajax(request: HttpRequest) -> bool:
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def fetchQuote():
    quotes = [
        "If you prick us, do we not bleed? - Shakespeare",
        "When small men begin to cast big shadows, the sun is about to set. - Lin Yutang",
        "In the end I don't care if you love me or you hate me, just as long as I win. - House Of Cards",
        "Don't take the temperature for too long; you may forget to note down the values.",
        "You can beat 40 scholars with one fact, but you can't beat an idiot with 40 facts. - Mevlana",
        "A leader is best when people barely know he exists, when his work is done, his aim fulfilled, they will say: we did it ourselves. - Lao Tzu",
        "If the only tool you have is a hammer, everything looks like a nail.",
        "The man who asks a question is a fool for a minute, the man who does not ask is a fool for life. - Confucious",
        "Yesterday, I was clever, so I wanted to change the world. Today, I am cleverer, so I am changing myself.",
    ]

    quote = random.choice(quotes)

    return quote

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
    def getPostsByCategory(user: User, category: Category, pageNo, number_of_posts: int) -> list:
        if user.is_superuser:
            posts = BlogPost.objects.filter(Q(categories__name__icontains=category))
        else:
            posts = BlogPost.objects.filter(Q(categories__name__icontains=category) & Q(password_protect=False))

        paginatorInstance = Paginator(posts, number_of_posts)

        try:
            postsPage = paginatorInstance.get_page(pageNo)
        except PageNotAnInteger:
            postsPage = paginatorInstance.get_page(1)
        except EmptyPage:
            postsPage = paginatorInstance.get_page(paginatorInstance.num_pages)
            postsPage.adjusted_elided_pages = paginatorInstance.get_elided_page_range(pageNo)
        return postsPage


    """Get posts related to the post having the given slug."""
    @staticmethod
    def getRelatedPosts(user: User, slug) -> list:
        # get the original post and all its categories
        post = get_object_or_404(BlogPost, slug=slug)
        categories = set(post.categories.all()) # using set to avoid duplicates

        related_posts = set() # using set again to avoid duplicates

        # if req is made by superuser, private posts should also be shown
        # else, only public posts should be included
        if user.is_superuser:
            for category in categories:
                related_posts.update(BlogPost.objects.filter(categories__name__icontains=category).exclude(slug=slug))
        else:
            for category in categories:
                related_posts.update(BlogPost.objects.filter(Q(categories__name__icontains=category) & Q(password_protect=False)).exclude(slug=slug))

        # convert `related_posts` to list in order to use `sort()`
        related_posts = list(related_posts)

        # get the max no of categories 
        def longest_category_count(post):
            return sum(1 for category in categories if category in post.categories.all())

        # sort such that the posts matching most closely to the original post rank higher
        related_posts.sort(key=longest_category_count, reverse=True)

        return related_posts

class BlogDetail:
    @staticmethod
    def getBlogDetailAdminView(request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        if post.password_protect:
            if request.user.is_superuser:
                pass
            else:
                return render(request, 'core/error/403.html', status=403)

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
