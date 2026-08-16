from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve as static_serve

from lab.misconfig_views import internal_backup, robots_txt

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("shop.urls")),
    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("reviews/", include("reviews.urls")),
    path("seller/", include("sellerpanel.urls")),
    path("support/", include("support.urls")),
    path("lab/", include("lab.urls")),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("internal-backup/", internal_backup, name="internal_backup"),
    path(
        "media/<path:path>",
        static_serve,
        {"document_root": settings.MEDIA_ROOT},
        name="media",
    ),
    path(
        "static/<path:path>",
        static_serve,
        {"document_root": settings.BASE_DIR / "static"},
        name="static",
    ),
]
