import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('Live In NBO')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-newsletter-every-monday-morning': {
        'task': 'newsletter.tasks.send_weekly_newsletter',  
        'schedule': app.crontab(hour=9, minute=0, day_of_week='monday'),
    },
}
