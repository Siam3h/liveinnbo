from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .services import get_upcoming_events, get_recent_blog_posts
from celery import shared_task


def send_newsletter():
    """Sends the weekly newsletter to subscribed users."""
    users = User.objects.filter(newsletter__subscribed=True)  # Fetch subscribed users

    events = get_upcoming_events()
    blog_posts = get_recent_blog_posts()

    # Generate email content from template
    html_content = render_to_string('newsletter/email.html', {
        'events': events,
        'blog_posts': blog_posts
    })

    subject = 'Weekly Newsletter: Upcoming Events and Recent Posts'
    from_email = settings.DEFAULT_FROM_EMAIL

    for user in users:
        to_email = user.email
        email = EmailMultiAlternatives(subject, "", from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()

@shared_task
def send_weekly_newsletter():
    send_newsletter()
