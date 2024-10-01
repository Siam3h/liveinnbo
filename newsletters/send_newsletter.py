from django.core.management.base import BaseCommand
from newsletters.tasks import send_newsletter

class Command(BaseCommand):
    help = 'Sends weekly newsletter'

    def handle(self, *args, **kwargs):
        send_newsletter()
        self.stdout.write(self.style.SUCCESS('Newsletter sent successfully'))
