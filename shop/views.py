from django.db import connection
from django.shortcuts import get_object_or_404, render

from .models import Brand, Category, Product


def home(request):
    featured = Product.objects.order_by("-rating_avg")[:8]
    categories = Category.objects.all()
    return render(request, "shop/home.html", {"featured": featured, "categories": categories})


def catalog(request):
    products = Product.objects.select_related("category", "brand").all()

    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    brand_id = request.GET.get("brand")
    if brand_id and brand_id.isdigit():
        products = products.filter(brand_id=brand_id)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and min_price.replace(".", "", 1).isdigit():
        products = products.filter(price__gte=min_price)
    if max_price and max_price.replace(".", "", 1).isdigit():
        products = products.filter(price__lte=max_price)

    sort = request.GET.get("sort", "-created_at")
    if sort in {"price", "-price", "-rating_avg", "-created_at"}:
        products = products.order_by(sort)

    return render(request, "shop/catalog.html", {
        "products": products,
        "categories": Category.objects.all(),
        "brands": Brand.objects.all(),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, "shop/product_detail.html", {"product": product, "related": related})


def search(request):
    """
    === INTENTIONAL VULNERABILITY: A05:2025 - Injection (SQL) ===
    See instructor_solutions/A05-INJECTION.md

    The query string is interpolated directly into raw SQL instead of using
    the ORM or parameterized query placeholders, allowing classic UNION-
    based SQL injection against the SQLite database, including reading the
    unrelated lab_flagvault table.
    """
    q = request.GET.get("q", "")
    results = []
    error = None
    if q:
        raw_sql = (
            "SELECT id, name, price FROM shop_product "
            f"WHERE name LIKE '%{q}%' OR description LIKE '%{q}%'"
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_sql)
                columns = [c[0] for c in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as exc:
            error = str(exc)

    return render(request, "shop/search.html", {"q": q, "results": results, "error": error})
