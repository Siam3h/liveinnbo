from django.core import paginator
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from django.http import Http404
from events.models import Event
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
import random
import re
from django.views.decorators.cache import cache_page

@cache_page(60 * 20)
def events(request):
    events = Event.objects.all().order_by('-created_at')
    categories = Event.objects.values_list('category', flat=True).distinct()
    for event in events:
        event.price_in_kobo = int(event.price * 100)
    paginator = Paginator(events, 15)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    context = {'events': events, 'categories': categories}
    return render(request, 'events/events.html', context)

@cache_page(60 * 20)
def category(request, category):
    category_events = Event.objects.filter(category=category).order_by('-created_at')
    if not category_events:
        message = f"No events found in category: {category}"
        return render(request, "events/category.html", {"message": message})
    paginator = Paginator(category_events, 15)
    page = request.GET.get('page')
    category_events = paginator.get_page(page)
    return render(request, "events/category.html", {"category":category, "category_events":category_events})

@cache_page(60 * 20)
def categories(request):
    all_categories = Event.objects.values('category').distinct().order_by('category')
    return render(request, "events/categories.html", {'all_categories': all_categories})


def search(request):
    query = request.GET.get('q')
    query_list = query.split()
    results = Event.objects.none()
    for word in query_list:
        results = results | Event.objects.filter(Q(title__contains=word) | Q(content__contains=word)).order_by('-created_at')
    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    if len(results) == 0:
        message = "Sorry, no results found for your search query."
    else:
        message = ""
    return render(request, 'events/search.html', {'results': results, 'query': query, 'message': message})


@cache_page(60 * 20)
def event_detail(request, event_id):
    try:
        events = get_object_or_404(Event, id=event_id)
        context = {'events': events}
        return render(request, 'events/eventspost.html', context)
    except Event.DoesNotExist:
        context = {'message': 'Event detail not found'}
        return render(request, 'events/404.html', context, status=404)


