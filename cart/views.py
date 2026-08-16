from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from shop.models import Product

from .cart import Cart


def view(request):
    cart = Cart(request)
    return render(request, "cart/view.html", {"cart_items": list(cart.items()), "total": cart.total()})


def add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get("quantity", "1")
    quantity = int(quantity) if quantity.lstrip("-").isdigit() else 1
    Cart(request).add(product.id, quantity)
    messages.success(request, f"{product.name} savatchaga qo'shildi.")
    return redirect("cart:view")


def update(request, product_id):
    quantity_raw = request.POST.get("quantity", "1")
    try:
        quantity = int(quantity_raw)
    except ValueError:
        quantity = 1
    Cart(request).set_quantity(product_id, quantity)
    return redirect("cart:view")


def remove(request, product_id):
    Cart(request).remove(product_id)
    return redirect("cart:view")
