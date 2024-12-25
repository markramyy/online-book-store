from django.urls import path
from store.views import *

urlpatterns = [
    # Custom views
    path('books/', book_list, name='book_list'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/', add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart/remove/', remove_cart_item, name='remove_cart_item'),
    path('checkout/', checkout, name='checkout'),
    path('orders/history/', order_history, name='order_history'),
    path('orders/cancel/', cancel_order, name='cancel_order'),
    path('books/<int:book_id>/add_review/', add_review, name='add_review'),
    path('dashboard/', customer_dashboard, name='customer_dashboard'),
    path('notify-user/', notify_user, name='notify_user'),

    # Admin views
    path('admin/dashboard', admin_dashboard, name='admin_dashboard'),
    path('admin/books/', manage_books, name='manage_books'),
    path('admin/books/add/', add_book, name='add_book'),
    path('admin/books/<int:book_id>/edit/', edit_book, name='edit_book'),
    path('admin/books/<int:book_id>/delete/', delete_book, name='delete_book'),
    path('admin/orders/', manage_orders, name='manage_orders'),
    path('admin/orders/<int:order_id>/confirm/', confirm_order, name='confirm_order'),
    path('admin/orders/<int:order_id>/cancel/', cancel_order_admin, name='cancel_order_admin'),
]
