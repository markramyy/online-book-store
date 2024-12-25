from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Book
from random import randint, choice

class Command(BaseCommand):
    help = 'Load mock data for testing the project'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@admin.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))

        # Create customers
        customers = [
            {'username': 'customer1', 'email': 'customer1@example.com', 'password': 'password123'},
            {'username': 'customer2', 'email': 'customer2@example.com', 'password': 'password123'},
        ]

        for customer in customers:
            if not User.objects.filter(username=customer['username']).exists():
                user = User.objects.create_user(
                    username=customer['username'],
                    email=customer['email'],
                    password=customer['password'],
                )
                user.is_customer = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully created customer {customer['username']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Customer {customer['username']} already exists"))

        # Create admin users
        admins = [
            {'username': 'admin1', 'email': 'admin1@example.com', 'password': 'password123'},
            {'username': 'admin2', 'email': 'admin2@example.com', 'password': 'password123'},
        ]

        for admin in admins:
            if not User.objects.filter(username=admin['username']).exists():
                user = User.objects.create_user(
                    username=admin['username'],
                    email=admin['email'],
                    password=admin['password'],
                )
                user.is_admin = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully created admin {admin['username']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Admin {admin['username']} already exists"))

        # Create mock books
        categories = ['fiction', 'non_fiction', 'science', 'history', 'fantasy', 'mystery', 'romance']
        authors = ['Author A', 'Author B', 'Author C', 'Author D', 'Author E']

        for i in range(10):  # Create 10 books
            title = f"Book {i + 1}"
            author = choice(authors)
            category = choice(categories)
            price = randint(10, 100)
            stock = randint(1, 50)
            popularity = randint(0, 100)
            edition = f"Edition {randint(1, 5)}"

            if not Book.objects.filter(title=title).exists():
                Book.objects.create(
                    title=title,
                    author=author,
                    category=category,
                    price=price,
                    stock=stock,
                    popularity=popularity,
                    edition=edition,
                )
                self.stdout.write(self.style.SUCCESS(f"Successfully created book '{title}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Book '{title}' already exists"))
