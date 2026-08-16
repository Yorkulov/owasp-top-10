from django.urls import path

from . import views

app_name = "lab"

urlpatterns = [
    path("progress/", views.progress, name="progress"),
    path("hint/<str:vuln_id>/unlock/", views.unlock_hint, name="unlock_hint"),
    path("submit/", views.submit_flag, name="submit_flag"),
    path("internal/flag-vault/", views.internal_flag_vault, name="internal_flag_vault"),
]
