from django.contrib import admin
from .models import Book, Order, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock', 'popularity')
    list_filter = ('category',)
    search_fields = ('title', 'author')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'book__title')
