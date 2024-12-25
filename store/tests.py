from django.test import TestCase
from django.contrib.auth.models import User

from .models import Book, Order
from .utils import AppConfigSingleton
from .factories import NotificationFactory, EmailNotification, SMSNotification
from .decorators import RegularBook, DiscountDecorator


class BookModelTest(TestCase):
    def test_book_creation(self):
        book = Book.objects.create(
            title="Example Book",
            author="Author Name",
            category="non_fiction",
            price=19.99,
            stock=10,
            popularity=0
        )
        self.assertEqual(book.title, "Example Book")
        self.assertEqual(book.stock, 10)

class OrderModelTest(TestCase):
    def test_order_creation(self):
        user = User.objects.create(username="testuser")
        book = Book.objects.create(
            title="Physics 101",
            author="Jane Doe",
            category="science",
            price=15.99,
            stock=5
        )
        order = Order.objects.create(user=user, book=book, quantity=2, status="pending")
        self.assertEqual(order.total_price(), 31.98)
        self.assertEqual(order.status, "pending")


# Singleton Design Pattern
class SingletonPatternTest(TestCase):
    def test_singleton_instance(self):
        instance1 = AppConfigSingleton()
        instance2 = AppConfigSingleton()
        self.assertEqual(instance1, instance2)
        self.assertEqual(instance1.get_config(), instance2.get_config())


# Factory Design Pattern Test
class FactoryPatternTest(TestCase):
    def test_email_notification(self):
        notification = NotificationFactory.create_notification("email")
        self.assertIsInstance(notification, EmailNotification)
        notification.send("Test email message")

    def test_sms_notification(self):
        notification = NotificationFactory.create_notification("sms")
        self.assertIsInstance(notification, SMSNotification)
        notification.send("Test SMS message")

    def test_invalid_notification(self):
        with self.assertRaises(ValueError):
            NotificationFactory.create_notification("push")


# Decorator Design Pattern
class DecoratorPatternTest(TestCase):
    def test_discounted_price(self):
        book = RegularBook(100)
        discounted_book = DiscountDecorator(book, 0.20)
        self.assertEqual(discounted_book.get_price(), 80)

    def test_regular_price(self):
        book = RegularBook(100)
        self.assertEqual(book.get_price(), 100)
