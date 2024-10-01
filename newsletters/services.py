import random
from django.utils import timezone
from datetime import timedelta
from events.models import Event  
from blogs.models import BlogPost  

def get_upcoming_events():
    """Fetches upcoming events in the next week."""
    today = timezone.now().date()
    next_week = today + timedelta(weeks=1)
    
    return Event.objects.filter(date__gte=today, date__lte=next_week)

def get_recent_blog_posts():
    """Fetch random blog posts from the past two weeks."""
    two_weeks_ago = timezone.now() - timedelta(weeks=2)
    
    posts = BlogPost.objects.filter(published_date__gte=two_weeks_ago)
    random_posts = random.sample(list(posts), min(len(posts), 2)) 
    return random_posts
