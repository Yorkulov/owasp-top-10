from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("paid", "To'landi"),
        ("shipped", "Jo'natildi"),
        ("delivered", "Yetkazildi"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    shipping_address = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
