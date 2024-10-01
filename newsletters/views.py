from django.shortcuts import redirect
from .models import Newsletter

def subscribe(request):
    if request.user.is_authenticated:
        newsletter, created = Newsletter.objects.get_or_create(user=request.user)
        newsletter.subscribed = True
        newsletter.save()
    return redirect('home')

def unsubscribe(request):
    if request.user.is_authenticated:
        newsletter = Newsletter.objects.get(user=request.user)
        newsletter.subscribed = False
        newsletter.save()
    return redirect('home')
