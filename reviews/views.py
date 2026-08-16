from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from shop.models import Product

from .models import Review


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        rating = request.POST.get("rating", "5")
        comment = request.POST.get("comment", "")
        Review.objects.create(
            product=product,
            user=request.user,
            rating=int(rating) if rating.isdigit() else 5,
            comment=comment,
        )
        messages.success(request, "Sharh qo'shildi.")
    return redirect("shop:product_detail", slug=slug)
