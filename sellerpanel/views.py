import urllib.error
import urllib.request

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from lab.internal import INTERNAL_HEADER, INTERNAL_HEADER_VALUE
from orders.models import Order
from shop.models import Product


def _is_seller(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role in {"seller", "admin"}


@login_required
def dashboard(request):
    if not _is_seller(request.user):
        messages.error(request, "Bu bo'lim faqat sotuvchilar uchun.")
        return redirect("shop:home")
    products = Product.objects.all().order_by("-created_at")[:50]
    orders = Order.objects.all().order_by("-created_at")[:50]
    return render(request, "sellerpanel/dashboard.html", {"products": products, "orders": orders})


@login_required
def import_image(request, product_id):
    """
    === INTENTIONAL VULNERABILITY: A01:2025 - Broken Access Control (SSRF) ===
    See instructor_solutions/A01-BAC-SSRF.md

    Fetches whatever URL the seller supplies, server-side, with no
    allow-list restricting it to public image hosts. A malicious/curious
    seller can point it at internal-only services (e.g.
    http://127.0.0.1:<port>/lab/internal/flag-vault/) that are not meant to
    be reachable directly from the browser.
    """
    if not _is_seller(request.user):
        messages.error(request, "Bu bo'lim faqat sotuvchilar uchun.")
        return redirect("shop:home")

    product = get_object_or_404(Product, id=product_id)
    fetched_preview = None

    if request.method == "POST":
        image_url = request.POST.get("image_url", "").strip()
        if image_url:
            try:
                req = urllib.request.Request(
                    image_url, headers={INTERNAL_HEADER: INTERNAL_HEADER_VALUE}
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    body = resp.read(2000)
                fetched_preview = body.decode(errors="replace")
                product.image_url = image_url
                product.image_note = "URL orqali import qilindi"
                product.save()
            except urllib.error.URLError as exc:
                fetched_preview = f"Xatolik: {exc}"

    return render(request, "sellerpanel/import_image.html", {
        "product": product, "fetched_preview": fetched_preview,
    })
