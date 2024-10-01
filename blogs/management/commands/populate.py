from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blogs.models import Blog
from events.models import Event
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data.'

    def handle(self, *args, **kwargs):
        self.populate_users()
        self.populate_events()
        self.populate_blogs()

    def populate_users(self):
        usernames = ['user1', 'user2', 'user3', 'user4', 'user5']
        for username in usernames:
            if not User.objects.filter(username=username).exists():  # Check if the user already exists
                user = User.objects.create_user(
                    username=username,
                    password='password123',
                    email=f'{username}@example.com'
                )
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User {username} created.'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists.'))


    def populate_events(self):
        titles = [
            'Concert in ',
            'Exhibition',
            'Tech ',
            ' Festival',
            'Charity'
        ]
        for title in titles:
            event = Event.objects.create(
                title=title,
                content=f'Details about {title}.',
                category=random.choice(['Music', 'Art', 'Technology', 'Food']),
                created_at=random.choice(['2023-01-01', '2023-06-15', '2023-12-31']),
                price=random.choice(['500', '1500', '600'])
            )
            event.save()
            self.stdout.write(self.style.SUCCESS(f'Event "{title}" created.'))

    def populate_blogs(self):
        titles = [
            'First Blog Post',
            'Second Blog Post',
            'Third Blog Post',
            'Another Interesting Post',
            'Last Blog Post'
        ]
        for title in titles:
            slug = slugify(title)  # Generate a slug from the title
            if Blog.objects.filter(slug=slug).exists():
                # If slug exists, append a random number to create a unique slug
                slug = f"{slug}-{random.randint(1, 1000)}"
            
            blog = Blog.objects.create(
                title=title,
                meta="A sample meta description for SEO.",
                content="This is the blog content.",
                thumbnail_url="https://via.placeholder.com/150",
                category="Uncategorized",
                slug=slug
            )
            blog.save()
            self.stdout.write(self.style.SUCCESS(f'Blog "{title}" created with slug: {slug}.'))

    # Other population functions (users, events)...
