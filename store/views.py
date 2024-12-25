from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse

from store.models import Book, Order, CATEGORY_CHOICES, CartItem
from store.utils import get_or_create_cart, add_to_cart, remove_from_cart, AppConfigSingleton
from store.forms import ReviewForm, BookForm
from store.factories import NotificationFactory
from store.decorators import RegularBook, DiscountDecorator, TaxDecorator

from users.middleware import customer_required, admin_required


@login_required
@customer_required
def book_list(request):
    books = Book.objects.all()

    for book in books:
        regular_book = RegularBook(book.price)
        discounted_book = DiscountDecorator(regular_book, 0.1)
        taxed_book = TaxDecorator(discounted_book, 0.05)
        book.final_price = taxed_book.get_price()

    # Search
    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # Filter by category
    category = request.GET.get('category')
    if category:
        books = books.filter(category=category)

    # Sort by price or popularity
    sort_by = request.GET.get('sort_by')
    if sort_by in ['price', '-price', 'popularity', '-popularity']:
        books = books.order_by(sort_by)

    # Pagination
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    categories = CATEGORY_CHOICES
    return render(request, 'store/customer/book_list.html', {'books': books, 'categories': categories})


@login_required
@customer_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'store/customer/cart.html', {'cart': cart, 'items': cart_items})


@login_required
@customer_required
def add_to_cart_ajax(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        config = AppConfigSingleton()
        default_quantity = config.get_config().get("default_cart_quantity", 1)
        quantity = int(request.POST.get('quantity', default_quantity))
        cart = get_or_create_cart(request.user)
        book = get_object_or_404(Book, id=book_id)
        add_to_cart(cart, book, quantity)
        return JsonResponse({'success': True, 'message': f'{book.title} has been added to your cart.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)


@login_required
@customer_required
def remove_cart_item(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request.user)
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        remove_from_cart(cart, book)
        return redirect('cart_view')


@login_required
@customer_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    if not cart.cartitem_set.exists():
        return render(request, 'store/customer/checkout.html', {'error': 'Your cart is empty. Add items before proceeding to checkout.'})

    # Create orders for each cart item
    for item in cart.cartitem_set.all():
        Order.objects.create(
            user=request.user,
            book=item.book,
            quantity=item.quantity,
            status='pending'
        )
    cart.cartitem_set.all().delete()  # Clear the cart
    return render(request, 'store/customer/checkout.html', {'success': 'Your order has been placed successfully!'})


@login_required
@customer_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'store/customer/order_history.html', {'orders': orders})


@login_required
@customer_required
def cancel_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=request.user, status='pending')
        order.delete()
        return redirect('order_history')
    else:
        return render(request, 'store/customer/order_history.html', {'error': 'Invalid request. Please try again.'})


@login_required
@customer_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'There was an error with your submission. Please correct it and try again.')
    else:
        form = ReviewForm()
    return render(request, 'store/customer/add_review.html', {'form': form, 'book': book})


@login_required
@customer_required
def customer_dashboard(request):
    return render(request, 'users/customer_dashboard.html')


@login_required
@customer_required
def notify_user(request):
    notification_type = request.GET.get('type', 'email')  # 'email' or 'sms'
    use_proxy = True  # Enable the proxy to rate-limit notifications

    notification = NotificationFactory.create_notification(notification_type, use_proxy=use_proxy)
    recipient = request.user.email if notification_type == 'email' else '123-456-7890'
    message = "This is a test notification."

    notification.send(message, recipient)
    return JsonResponse({'success': True, 'message': 'Notification sent.'})


@login_required
@admin_required
def manage_books(request):
    books = Book.objects.all()
    return render(request, 'store/admin/manage_books.html', {'books': books})


@login_required
@admin_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm()
    return render(request, 'store/admin/add_book.html', {'form': form})


@login_required
@admin_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'store/admin/edit_book.html', {'form': form, 'book': book})


@login_required
@admin_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('manage_books')
    return render(request, 'store/admin/delete_book.html', {'book': book})


@login_required
@admin_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'store/admin/manage_orders.html', {'orders': orders})


@login_required
@admin_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'confirmed'
    order.save()

    notification = NotificationFactory.create_notification("email")
    notification.send(f"Your order for {order.book.title} has been confirmed.", order.user.email)

    return redirect('manage_orders')


@login_required
@admin_required
def cancel_order_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('manage_orders')


@login_required
@admin_required
def admin_dashboard(request):
    top_books = Book.objects.order_by('-popularity')[:5]
    top_categories = Book.objects.values('category').annotate(total=Sum('popularity')).order_by('-total')[:5]
    return render(request, 'users/admin_dashboard.html', {'top_books': top_books, 'top_categories': top_categories})
