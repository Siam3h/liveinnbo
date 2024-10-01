from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from django.http import Http404
from blogs.models import Blog
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
import random
import re
from django.views.decorators.cache import cache_page


@cache_page(60 * 20)
def blog(request):
    blogs = Blog.objects.filter(is_approved=True).order_by('-time')  
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    context = {'blogs': blogs}
    return render(request, 'blogs/blog.html', context)

@cache_page(60 * 20)
def category(request, category):
    category_posts = Blog.objects.filter(category=category).exclude(slug__isnull=True).exclude(slug__exact='').order_by('-time')
    if not category_posts:
        message = f"No posts found in category: '{category}'"
        return render(request, "blogs/category.html", {"message": message})

    paginator = Paginator(category_posts, 3)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)
    return render(request, "blogs/category.html", {"category": category, 'category_posts': category_posts})

@cache_page(60 * 20)
def categories(request):
    all_categories = Blog.objects.values('category').distinct().order_by('category')
    return render(request, "blogs/categories.html", {'all_categories': all_categories})


def search(request):
    query = request.GET.get('q', '') 

    if query:
        query_list = query.split()
        results = Blog.objects.none()
        for word in query_list:
            results |= Blog.objects.filter(Q(title__icontains=word) | Q(content__icontains=word)).order_by('-time')
        paginator = Paginator(results, 3)  
        page = request.GET.get('page')
        results = paginator.get_page(page)
        if not results:
            message = f"Sorry, no results found for '{query}'."
        else:
            message = ""
    else:
        results = None
        message = "Please enter a search term."
    context = {
        'results': results,
        'query': query,
        'message': message,
    }
    return render(request, 'blogs/search.html', context)




@cache_page(60 * 20)
def blogpost(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    previous_blog = Blog.objects.filter(is_approved=True, time__lt=blog.time).order_by('-time').first()
    next_blog = Blog.objects.filter(is_approved=True, time__gt=blog.time).order_by('time').first()
    
    context = {
        'blog': blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
    }
    
    return render(request, 'blogs/blogpost.html', context)
