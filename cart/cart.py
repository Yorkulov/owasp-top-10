from decimal import Decimal

from shop.models import Product

SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_KEY)
        if cart is None:
            cart = {}
            self.session[SESSION_KEY] = cart
        self.cart = cart

    def add(self, product_id, quantity):
        pid = str(product_id)
        self.cart[pid] = self.cart.get(pid, 0) + quantity
        self.save()

    def set_quantity(self, product_id, quantity):
        pid = str(product_id)
        self.cart[pid] = quantity
        self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[SESSION_KEY] = {}
        self.save()

    def items(self):
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.in_bulk(product_ids)
        for pid, qty in self.cart.items():
            product = products.get(int(pid))
            if product:
                yield {
                    "product": product,
                    "quantity": qty,
                    "subtotal": product.price * Decimal(qty),
                }

    def total(self):
        return sum((item["subtotal"] for item in self.items()), Decimal("0"))

    def __len__(self):
        return len(self.cart)
