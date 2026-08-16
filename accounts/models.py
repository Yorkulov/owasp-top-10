from django.contrib.auth.models import User
from django.db import models

ROLE_CHOICES = [
    ("customer", "Xaridor"),
    ("seller", "Sotuvchi"),
    ("admin", "Administrator"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="customer")
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
