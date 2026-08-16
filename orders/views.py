from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from lab.flags import compute_flag

from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == "POST":
        address = request.POST.get("address", "")
        total = cart.total()

        notes = ""
        if total <= 0 and len(cart) > 0:
            # === INTENTIONAL VULNERABILITY: A06:2025 - Insecure Design ===
            # See instructor_solutions/A06-INSECURE-DESIGN.md
            # Negative-quantity cart items (see cart/cart.py) can drive the
            # order total to zero or below. The checkout should reject this,
            # but instead happily "completes" a free/negative order.
            notes = compute_flag("A06-INSECURE-DESIGN")

        order = Order.objects.create(
            user=request.user, shipping_address=address,
            total=total, status="paid", notes=notes,
        )
        for item in cart.items():
            OrderItem.objects.create(
                order=order, product_name=item["product"].name,
                unit_price=item["product"].price, quantity=item["quantity"],
            )
        cart.clear()
        messages.success(request, "Buyurtma rasmiylashtirildi!")
        return redirect("orders:detail", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "cart_items": list(cart.items()), "total": cart.total(),
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    """
    === INTENTIONAL VULNERABILITY: A01:2025 - Broken Access Control (IDOR) ===
    See instructor_solutions/A01-BAC-IDOR.md

    Any authenticated user can view ANY order by guessing/incrementing the
    numeric ID in the URL - there is no check that order.user == request.user.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/detail.html", {"order": order})


@login_required
def order_invoice(request, order_id):
    """
    === INTENTIONAL VULNERABILITY: A10:2025 - Mishandling of Exceptional Conditions ===
    See instructor_solutions/A10-EXCEPTIONS.md

    The permission check below is wrapped in an overly broad try/except
    that "fails open": ANY exception while resolving/authorizing the order
    (e.g. a non-numeric order_id) falls through to returning a fallback
    order instead of denying access.
    """
    try:
        order = Order.objects.get(id=int(order_id))
        if order.user_id != request.user.id:
            raise PermissionError("not your order")
    except Exception:
        order = Order.objects.filter(user__username="_exceptions_target").first()

    return render(request, "orders/invoice.html", {"order": order})
