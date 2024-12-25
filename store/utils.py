from store.models import Cart, CartItem


class AppConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfigSingleton, cls).__new__(cls)
            cls._config = {"app_name": "OnlineBookStore", "default_cart_quantity": 1}
        return cls._instance

    def get_config(self):
        return self._config

    def set_config(self, key, value):
        self._config[key] = value


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def add_to_cart(cart, book, quantity=1):
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += quantity
    item.save()
    print(f"Added to cart: {book.title}, Quantity: {item.quantity}")
    return item


def remove_from_cart(cart, book):
    CartItem.objects.filter(cart=cart, book=book).delete()
