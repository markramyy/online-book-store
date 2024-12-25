from django.db import models

from users.models import User


CATEGORY_CHOICES = [
    ('fiction', 'Fiction'),
    ('non_fiction', 'Non-Fiction'),
    ('science', 'Science'),
    ('history', 'History'),
    ('biography', 'Biography'),
    ('fantasy', 'Fantasy'),
    ('mystery', 'Mystery'),
    ('romance', 'Romance'),
]


class Book(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='fiction')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(null=True, blank=True)
    popularity = models.IntegerField(default=0)
    edition = models.CharField(max_length=50, null=True, blank=True)
    cover_image = models.ImageField(upload_to='books/covers/', null=True, blank=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped')
    ], default='pending')

    def total_price(self):
        return self.book.price * self.quantity


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.book.price * self.quantity
