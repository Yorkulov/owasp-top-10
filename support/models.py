from django.contrib.auth.models import User
from django.db import models


class SupportMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_messages")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
