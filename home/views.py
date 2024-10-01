from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
import random
import re
from blogs.models import Blog  
from events.models import Event 
from django.views.decorators.cache import cache_page

@cache_page(60 * 20)
def index(request):
    blogs = Blog.objects.filter(is_approved=True).order_by('-time')[:3]
    events = Event.objects.all().order_by('-created_at')[:3]
    for event in events:
        event.price_in_kobo = int(event.price * 100)
    context = {'events': events, 'blogs': blogs}
    return render(request, 'home/index.html',context)

@cache_page(60 * 20)
def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        invalid_imput = ['', ' ']
        
        
        if name in invalid_imput or email in invalid_imput or phone in invalid_imput or message in invalid_imput:
            messages.error(request, 'One or more fields are empty!')
        else:
            email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            phone_pattern = re.compile(r'^[0-9]{10}$')

            if email_pattern.match(email) and phone_pattern.match(phone):
                form_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'message': message,
                }

                formatted_message = f"""
                From: {form_data['name']}
                Message: {form_data['message']}
                Email: {form_data['email']}
                Phone: {form_data['phone']}
                """

                try:
                    send_mail(
                        'You got a mail!',
                        formatted_message,
                        '', 
                        ['nbo@outlook.com'],
                        fail_silently=False,
                    )
                    messages.success(request, 'Your message was sent successfully.')
                except Exception as e:
                    messages.error(request, f"An error occurred while sending your message: {e}")
            else:
                messages.error(request, 'Email or Phone is Invalid!')

    return render(request, 'home/contact.html', {})
