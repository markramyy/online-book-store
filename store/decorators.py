from decimal import Decimal

class Book:
    def get_price(self):
        raise NotImplementedError("Subclasses must implement the get_price method.")

class RegularBook(Book):
    def __init__(self, price):
        self.price = Decimal(price)

    def get_price(self):
        return self.price

class DiscountDecorator(Book):
    def __init__(self, book, discount):
        self.book = book
        self.discount = Decimal(discount)

    def get_price(self):
        return self.book.get_price() * (1 - self.discount)

class TaxDecorator(Book):
    def __init__(self, book, tax_rate):
        self.book = book
        self.tax_rate = Decimal(tax_rate)

    def get_price(self):
        return self.book.get_price() * (1 + self.tax_rate)
