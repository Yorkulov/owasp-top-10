from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("", views.order_list, name="list"),
    path("<int:order_id>/", views.order_detail, name="detail"),
    path("<str:order_id>/invoice/", views.order_invoice, name="invoice"),
]
