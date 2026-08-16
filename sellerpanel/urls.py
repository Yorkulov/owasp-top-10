from django.urls import path

from . import views

app_name = "sellerpanel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("product/<int:product_id>/import-image/", views.import_image, name="import_image"),
]
